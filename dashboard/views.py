from django.db.models import Q, Sum
from django.shortcuts import render

from accounts.decorators import admin_required
from activity_logs.models import ActivityLog
from appointments.models import Appointment
from businesses.utils import get_current_business
from customers.models import Customer
from employees.models import Employee
from invoices.models import Invoice
from orders.models import Order
from tasks.models import Task


def get_business_queryset(request, model):
    business = get_current_business(request)

    if request.user.is_superuser and business is None:
        return model.objects.all()

    return model.objects.filter(business=business)


@admin_required
def dashboard_view(request):
    business = get_current_business(request)

    customers = get_business_queryset(request, Customer)
    employees = get_business_queryset(request, Employee)
    orders = get_business_queryset(request, Order)
    invoices = get_business_queryset(request, Invoice)
    appointments = get_business_queryset(request, Appointment)
    tasks = get_business_queryset(request, Task)

    if request.user.is_superuser and business is None:
        activities = ActivityLog.objects.all()[:8]
    else:
        activities = ActivityLog.objects.filter(business=business)[:8]

    total_received = invoices.aggregate(total=Sum('paid_amount'))['total'] or 0
    total_pending_amount = invoices.aggregate(total=Sum('pending_amount'))['total'] or 0
    total_invoice_amount = invoices.aggregate(total=Sum('total_amount'))['total'] or 0
    total_order_amount = orders.aggregate(total=Sum('total_amount'))['total'] or 0

    task_summary = [
        {
            'label': 'Pending',
            'count': tasks.filter(status='Pending').count(),
            'class': 'warning',
        },
        {
            'label': 'In Progress',
            'count': tasks.filter(status='In Progress').count(),
            'class': 'info',
        },
        {
            'label': 'Completed',
            'count': tasks.filter(status='Completed').count(),
            'class': 'success',
        },
    ]

    order_summary = [
        {
            'label': 'Pending',
            'count': orders.filter(status='Pending').count(),
            'class': 'warning',
        },
        {
            'label': 'Processing',
            'count': orders.filter(status='Processing').count(),
            'class': 'info',
        },
        {
            'label': 'Completed',
            'count': orders.filter(status='Completed').count(),
            'class': 'success',
        },
        {
            'label': 'Cancelled',
            'count': orders.filter(status='Cancelled').count(),
            'class': 'danger',
        },
    ]

    invoice_summary = [
        {
            'label': 'Unpaid',
            'count': invoices.filter(status='Unpaid').count(),
            'class': 'warning',
        },
        {
            'label': 'Partial',
            'count': invoices.filter(status='Partial').count(),
            'class': 'info',
        },
        {
            'label': 'Paid',
            'count': invoices.filter(status='Paid').count(),
            'class': 'success',
        },
        {
            'label': 'Cancelled',
            'count': invoices.filter(status='Cancelled').count(),
            'class': 'danger',
        },
    ]

    context = {
        'business': business,

        'total_customers': customers.count(),
        'total_employees': employees.count(),
        'total_orders': orders.count(),
        'total_invoices': invoices.count(),
        'total_appointments': appointments.count(),
        'total_tasks': tasks.count(),

        'pending_tasks': tasks.filter(status='Pending').count(),
        'completed_tasks': tasks.filter(status='Completed').count(),

        'paid_invoices': invoices.filter(status='Paid').count(),
        'unpaid_invoices': invoices.filter(status='Unpaid').count(),

        'total_received': total_received,
        'total_pending_amount': total_pending_amount,
        'total_invoice_amount': total_invoice_amount,
        'total_order_amount': total_order_amount,

        'recent_customers': customers[:5],
        'recent_orders': orders.select_related('customer')[:5],
        'recent_invoices': invoices.select_related('customer')[:5],
        'recent_tasks': tasks.select_related('assigned_to')[:5],
        'recent_appointments': appointments.select_related('customer')[:5],
        'activities': activities,

        'task_summary': task_summary,
        'order_summary': order_summary,
        'invoice_summary': invoice_summary,
    }

    return render(request, 'dashboard/dashboard.html', context)


@admin_required
def global_search(request):
    business = get_current_business(request)
    q = request.GET.get('q', '').strip()

    customers = Customer.objects.none()
    employees = Employee.objects.none()
    tasks = Task.objects.none()
    orders = Order.objects.none()
    invoices = Invoice.objects.none()
    appointments = Appointment.objects.none()

    if q:
        if request.user.is_superuser and business is None:
            customers_base = Customer.objects.all()
            employees_base = Employee.objects.all()
            tasks_base = Task.objects.all()
            orders_base = Order.objects.all()
            invoices_base = Invoice.objects.all()
            appointments_base = Appointment.objects.all()
        else:
            customers_base = Customer.objects.filter(business=business)
            employees_base = Employee.objects.filter(business=business)
            tasks_base = Task.objects.filter(business=business)
            orders_base = Order.objects.filter(business=business)
            invoices_base = Invoice.objects.filter(business=business)
            appointments_base = Appointment.objects.filter(business=business)

        customers = customers_base.filter(
            Q(name__icontains=q) |
            Q(email__icontains=q) |
            Q(phone__icontains=q) |
            Q(company_name__icontains=q)
        )[:10]

        employees = employees_base.filter(
            Q(name__icontains=q) |
            Q(email__icontains=q) |
            Q(phone__icontains=q) |
            Q(position__icontains=q)
        )[:10]

        tasks = tasks_base.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(priority__icontains=q) |
            Q(status__icontains=q)
        )[:10]

        orders = orders_base.filter(
            Q(order_number__icontains=q) |
            Q(title__icontains=q) |
            Q(status__icontains=q) |
            Q(customer__name__icontains=q)
        ).select_related('customer')[:10]

        invoices = invoices_base.filter(
            Q(invoice_number__icontains=q) |
            Q(status__icontains=q) |
            Q(customer__name__icontains=q)
        ).select_related('customer')[:10]

        appointments = appointments_base.filter(
            Q(title__icontains=q) |
            Q(status__icontains=q) |
            Q(customer__name__icontains=q)
        ).select_related('customer')[:10]

    context = {
        'q': q,
        'customers': customers,
        'employees': employees,
        'tasks': tasks,
        'orders': orders,
        'invoices': invoices,
        'appointments': appointments,
    }

    return render(request, 'dashboard/global_search.html', context)


dashboard = dashboard_view