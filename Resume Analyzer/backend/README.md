Resume Analyzer (Flask)

Run:
- python -m venv .venv; .\.venv\Scripts\Activate; pip install -r requirements.txt
- set FLASK_APP=app.py; flask run

API:
- POST /api/upload (form-data file)
- POST /api/chat {message}
- GET /templates/simple_resume.docx
