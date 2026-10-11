# Lifeline – Pharmacy Management System

A modular web platform and healthcare portal built with Flask and SQLAlchemy designed to streamline retail pharmacy operations, medication tracking, and patient assistance.

---

## Key Features

- **Automated Inventory & Stock Tracking:** Real-time logging of pharmaceutical inventory, batch tracking, and low-stock indicators.
- **Relational Database Architecture:** Structured schema design with automated database migration handling via SQLAlchemy ORM.
- **Interactive Assistant:** Integrated chat interface to support customer queries and operational assistance.
- **Responsive Dashboard:** Intuitive front-end views for handling daily sales logs, prescription management, and inventory updates.

---

## Tech Stack & Architecture

- **Backend:** Python (Flask)
- **Database / ORM:** SQLite / MySQL, SQLAlchemy ORM
- **Frontend:** HTML5, CSS3, JavaScript, Jinja2 Templates
- **Architecture:** Modular MVC structure with RESTful routing

---

## Project Structure

```text
├── app.py                # Application entry point & core routing
├── check_db.py           # Database verification script
├── models.py             # SQLAlchemy database models & schemas
├── static/               # Custom CSS styles, JavaScript & assets
├── templates/            # Dynamic Jinja2 HTML templates
└── requirements.txt      # Python dependencies & packages
