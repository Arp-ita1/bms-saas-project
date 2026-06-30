# Business Management System - Django Project

A complete Django-based Business Management System for managing customers, employees, tasks, appointments, orders, invoices, notifications, business settings, and a customer portal.

## Tech Stack
- Python 3.8+
- Django 4.2+
- SQLite
- HTML, CSS, Bootstrap

## Setup

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Public website: http://127.0.0.1:8000/
- Admin dashboard: http://127.0.0.1:8000/dashboard/
- Django admin: http://127.0.0.1:8000/admin/

## Important Login Note
Use `python manage.py createsuperuser` to create an admin account. Normal registered users are treated as customers and redirected to the customer portal.


## Admin and Customer Access
- Admin pages require a staff/superuser account.
- Create admin using: `python manage.py createsuperuser`
- Normal registered users are customer users and can access only `/customer-portal/`.
