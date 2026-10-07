# services.py

from datetime import datetime
from models import tickets, technicians


def generate_ticket_number():
    """Generate a unique ticket number such as TKT-0001."""
    return f"TKT-{len(tickets) + 1:04d}"


def get_technicians():
    """Return the list of available technicians."""
    return technicians


def create_ticket(requester_name, category, description, priority):
    """Create a new support ticket."""
    
    ticket = {
        "ticket_number": generate_ticket_number(),
        "requester_name": requester_name,
        "category": category,
        "description": description,
        "priority": priority,
        "status": "Open",
        "assigned_technician": None,
        "date_created": datetime.now(),
        "date_resolved": None,
        "notes": []
    }

    tickets.append(ticket)

    return ticket


def find_ticket(ticket_number):
    """Find a ticket using its ticket number."""
    
    for ticket in tickets:
        if ticket["ticket_number"] == ticket_number:
            return ticket

    return None


def assign_technician(ticket_number, technician_id):
    """Assign a technician to a ticket."""
    
    ticket = find_ticket(ticket_number)

    if not ticket:
        return False, "Ticket not found."

    technician = next(
        (tech for tech in technicians if tech["id"] == technician_id),
        None
    )

    if not technician:
        return False, "Technician not found."

    ticket["assigned_technician"] = technician

    return True, "Technician assigned successfully."


def change_ticket_status(ticket_number, new_status):
    """Change a ticket's status while following the required workflow."""

    ticket = find_ticket(ticket_number)

    if not ticket:
        return False, "Ticket not found."

    current_status = ticket["status"]

    # Open → In Progress
    if current_status == "Open" and new_status == "In Progress":
        if ticket["assigned_technician"] is None:
            return False, "A technician must be assigned before starting the ticket."

    # In Progress → Resolved
    elif current_status == "In Progress" and new_status == "Resolved":
        ticket["date_resolved"] = datetime.now()

    # Resolved → In Progress
    elif current_status == "Resolved" and new_status == "In Progress":
        ticket["date_resolved"] = None

    # Resolved → Closed
    elif current_status == "Resolved" and new_status == "Closed":
        pass

    else:
        return False, f"Invalid status change: {current_status} → {new_status}"

    ticket["status"] = new_status

    return True, "Ticket status updated successfully."


def add_note(ticket_number, note_text, author):
    """Add a note to a ticket."""

    ticket = find_ticket(ticket_number)

    if not ticket:
        return False, "Ticket not found."

    note = {
        "text": note_text,
        "author": author,
        "timestamp": datetime.now()
    }

    # Newest notes will appear first
    ticket["notes"].insert(0, note)

    return True, "Note added successfully."


def get_resolution_days(ticket):
    """Calculate the number of days taken to resolve a ticket."""

    if not ticket["date_resolved"]:
        return None

    difference = ticket["date_resolved"] - ticket["date_created"]

    return difference.days


def get_dashboard_stats():
    """Return summary information for the dashboard."""

    total = len(tickets)

    open_count = sum(
        1 for ticket in tickets
        if ticket["status"] == "Open"
    )

    in_progress_count = sum(
        1 for ticket in tickets
        if ticket["status"] == "In Progress"
    )

    resolved_count = sum(
        1 for ticket in tickets
        if ticket["status"] == "Resolved"
    )

    closed_count = sum(
        1 for ticket in tickets
        if ticket["status"] == "Closed"
    )

    unassigned_open = sum(
        1 for ticket in tickets
        if ticket["status"] == "Open"
        and ticket["assigned_technician"] is None
    )

    return {
        "total": total,
        "open": open_count,
        "in_progress": in_progress_count,
        "resolved": resolved_count,
        "closed": closed_count,
        "unassigned_open": unassigned_open
    }