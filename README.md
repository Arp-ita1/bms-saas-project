# Business Management System - BMS SaaS

A multi-tenant Business Management System built using Django.  
This project allows different businesses to manage their customers, employees, tasks, orders, invoices, appointments and notifications from a single SaaS platform.

## Features

- Platform Admin Dashboard
- Business Registration and Subscription Plans
- Business Admin Dashboard
- Customer Management
- Employee Management
- Task Assignment
- Order Management
- Invoice Management
- Appointment Management
- Notification Management
- Employee Portal
- Customer Portal
- Role-based Login Redirect
- Multi-business Data Separation

## User Roles

### Platform Admin
Manages the complete SaaS platform, businesses, subscriptions and plans.

### Business Admin
Registers a business and manages business data such as customers, employees, tasks, orders and invoices.

### Employee
Logs in to employee portal and views assigned tasks.

### Customer
Logs in to customer portal and views personal orders and invoices.

## Tech Stack

- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap
- JavaScript

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER

Create virtual environment:

python -m venv venv

Activate virtual environment:

venv\Scripts\activate

Install requirements:

pip install -r requirements.txt

Run migrations:

python manage.py makemigrations
python manage.py migrate

Create superuser:

python manage.py createsuperuser

Run server:

python manage.py runserver

Open in browser:

http://127.0.0.1:8000/
Login Flow

All users login from the same login page:

/accounts/login/

Redirect based on role:

Platform Admin  -> /platform/
Business Admin  -> /dashboard/
Employee        -> /employee-portal/
Customer        -> /customer-portal/
Project Status

This project is developed as a final year academic project and can be extended with online payments, analytics, reports and deployment features.

Author

Arpita Sharma