# IT Help Desk

A starter Flask application for an IT help desk.

## Setup

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The application is available at <http://127.0.0.1:5000/>. The SQLite database is created at `data/helpdesk.db` when the application starts.

## Project structure

- `app.py`: Flask application entry point and page routes
- `database.py`: SQLite connection and initialization helpers
- `models.py`: Help desk data model definitions
- `services.py`: Ticket workflow and business logic
- `templates/`: HTML pages
- `static/`: CSS and JavaScript assets