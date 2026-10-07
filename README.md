# IT Help Desk Ticketing System

A campus IT Help Desk Ticketing System built to centralize the submission, tracking, assignment, and resolution of IT support requests.

The system allows staff and students to submit IT concerns while IT technicians can manage tickets, update their status, assign responsibilities, and add notes or updates.

## Features

- Submit new IT support tickets
- Automatically generate unique ticket numbers (TKT-XXXX)
- View and track submitted tickets
- Assign tickets to IT technicians
- Pre-populated IT technicians
- Update ticket status through a defined workflow
- Add notes and updates to tickets
- Search and filter tickets
- Sort tickets by priority or date
- View ticket details and resolution information
- Dashboard with ticket summary counts
- Track unresolved tickets without an assigned technician
- Calculate resolution time when a ticket is resolved

## Ticket Status Workflow

Tickets follow a defined lifecycle:

**Open → In Progress → Resolved → Closed**

- A ticket must have an assigned technician before it can move to **In Progress**.
- A **Resolved** ticket can be returned to **In Progress** if the issue is not fixed.
- Invalid status transitions are blocked by the system.

## Technologies

- Python
- Flask
- HTML
- CSS
- JavaScript
