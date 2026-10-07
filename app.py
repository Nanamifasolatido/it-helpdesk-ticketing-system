# app.py

from flask import Flask, render_template, request, redirect, url_for, flash

from models import tickets
from services import (
    create_ticket,
    find_ticket,
    get_technicians,
    assign_technician,
    change_ticket_status,
    add_note,
    get_resolution_days,
    get_dashboard_stats
)

app = Flask(__name__)
app.secret_key = "it415-helpdesk-secret"


# =========================
# =========================
# New Ticket Page
# =========================

@app.route("/tickets/new")
def new_ticket():
    return render_template("new_ticket.html")
# =========================

@app.route("/")
def dashboard():
    stats = get_dashboard_stats()

    return render_template(
        "dashboard.html",
        stats=stats
    )


# =========================
# Ticket List
# =========================

@app.route("/tickets")
def ticket_list():

    filtered_tickets = tickets.copy()

    # Search by keyword in ticket description
    search = request.args.get("search", "").strip()

    if search:
        filtered_tickets = [
            ticket for ticket in filtered_tickets
            if search.lower() in ticket["description"].lower()
        ]

    # Filter by status
    status = request.args.get("status", "")

    if status:
        filtered_tickets = [
            ticket for ticket in filtered_tickets
            if ticket["status"] == status
        ]

    # Filter by priority
    priority = request.args.get("priority", "")

    if priority:
        filtered_tickets = [
            ticket for ticket in filtered_tickets
            if ticket["priority"] == priority
        ]

    # Filter by category
    category = request.args.get("category", "")

    if category:
        filtered_tickets = [
            ticket for ticket in filtered_tickets
            if ticket["category"] == category
        ]

    # Filter by assigned technician
    technician = request.args.get("technician", "")

    if technician:
        filtered_tickets = [
            ticket for ticket in filtered_tickets
            if ticket["assigned_technician"]
            and str(ticket["assigned_technician"]["id"]) == technician
        ]

    # Sorting
    sort = request.args.get("sort", "date")

    if sort == "priority":
        priority_order = {
            "Critical": 1,
            "High": 2,
            "Medium": 3,
            "Low": 4
        }

        filtered_tickets.sort(
            key=lambda ticket: priority_order.get(
                ticket["priority"], 5
            )
        )

    else:
        # Newest tickets first
        filtered_tickets.sort(
            key=lambda ticket: ticket["date_created"],
            reverse=True
        )

    return render_template(
        "tickets.html",
        tickets=filtered_tickets,
        technicians=get_technicians()
    )


# =========================
# Create Ticket
# =========================

@app.route("/tickets/create", methods=["POST"])
def create_ticket_route():

    requester_name = request.form.get("requester_name", "").strip()
    category = request.form.get("category", "")
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "")

    if not requester_name or not category or not description or not priority:
        flash("Please complete all required fields.", "error")
        return redirect(url_for("ticket_list"))

    ticket = create_ticket(
        requester_name,
        category,
        description,
        priority
    )

    flash(
        f"Ticket {ticket['ticket_number']} created successfully.",
        "success"
    )

    return redirect(
        url_for(
            "ticket_detail",
            ticket_number=ticket["ticket_number"]
        )
    )


# =========================
# Ticket Detail
# =========================

@app.route("/tickets/<ticket_number>")
def ticket_detail(ticket_number):

    ticket = find_ticket(ticket_number)

    if not ticket:
        flash("Ticket not found.", "error")
        return redirect(url_for("ticket_list"))

    resolution_days = get_resolution_days(ticket)

    return render_template(
        "ticket_detail.html",
        ticket=ticket,
        technicians=get_technicians(),
        resolution_days=resolution_days
    )


# =========================
# Assign Technician
# =========================

@app.route(
    "/tickets/<ticket_number>/assign",
    methods=["POST"]
)
def assign_ticket_technician(ticket_number):

    technician_id = request.form.get("technician_id")

    if not technician_id:
        flash("Please select a technician.", "error")
        return redirect(
            url_for(
                "ticket_detail",
                ticket_number=ticket_number
            )
        )

    success, message = assign_technician(
        ticket_number,
        int(technician_id)
    )

    flash(
        message,
        "success" if success else "error"
    )

    return redirect(
        url_for(
            "ticket_detail",
            ticket_number=ticket_number
        )
    )


# =========================
# Change Ticket Status
# =========================

@app.route(
    "/tickets/<ticket_number>/status",
    methods=["POST"]
)
def update_ticket_status(ticket_number):

    new_status = request.form.get("status")

    success, message = change_ticket_status(
        ticket_number,
        new_status
    )

    flash(
        message,
        "success" if success else "error"
    )

    return redirect(
        url_for(
            "ticket_detail",
            ticket_number=ticket_number
        )
    )


# =========================
# Add Note
# =========================

@app.route(
    "/tickets/<ticket_number>/notes",
    methods=["POST"]
)
def add_ticket_note(ticket_number):

    note_text = request.form.get("note_text", "").strip()
    author = request.form.get("author", "").strip()

    if not note_text or not author:
        flash(
            "Please enter both the note and author.",
            "error"
        )

        return redirect(
            url_for(
                "ticket_detail",
                ticket_number=ticket_number
            )
        )

    success, message = add_note(
        ticket_number,
        note_text,
        author
    )

    flash(
        message,
        "success" if success else "error"
    )

    return redirect(
        url_for(
            "ticket_detail",
            ticket_number=ticket_number
        )
    )


# =========================
# Run Application
# =========================

if __name__ == "__main__":
    app.run(debug=True)