from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required
from activity_logs.utils import log_activity
from businesses.models import UserProfile
from businesses.utils import get_current_business

from .forms import EmployeeForm
from .models import Employee


def get_employee_queryset(request):
    business = get_current_business(request)

    if request.user.is_superuser and business is None:
        return Employee.objects.select_related('user', 'business').all()

    return Employee.objects.select_related('user', 'business').filter(business=business)


@admin_required
def employee_list(request):
    employees = get_employee_queryset(request)

    q = request.GET.get('q')
    if q:
        employees = employees.filter(
            Q(name__icontains=q) |
            Q(phone__icontains=q) |
            Q(email__icontains=q) |
            Q(position__icontains=q)
        )

    return render(request, 'employees/employee_list.html', {
        'employees': employees
    })


@admin_required
def employee_add(request):
    business = get_current_business(request)
    form = EmployeeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        employee = form.save(commit=False)
        employee.business = business

        create_login_account = form.cleaned_data.get('create_login_account')
        login_username = form.cleaned_data.get('login_username')
        login_password = form.cleaned_data.get('login_password')

        if create_login_account:
            user = User.objects.create_user(
                username=login_username,
                email=employee.email or '',
                password=login_password,
                first_name=employee.name
            )

            UserProfile.objects.create(
                user=user,
                business=business,
                role='Employee',
                phone=employee.phone
            )

            employee.user = user

        employee.save()

        log_activity(request.user, f'Added employee {employee.name}', 'Employees')
        messages.success(request, 'Employee added successfully.')
        return redirect('/employees/')

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Add Employee'
    })


@admin_required
def employee_edit(request, pk):
    employee = get_object_or_404(get_employee_queryset(request), pk=pk)
    form = EmployeeForm(request.POST or None, instance=employee)

    if request.method == 'POST' and form.is_valid():
        employee = form.save(commit=False)
        employee.business = employee.business or get_current_business(request)

        create_login_account = form.cleaned_data.get('create_login_account')
        login_username = form.cleaned_data.get('login_username')
        login_password = form.cleaned_data.get('login_password')

        if create_login_account and not employee.user:
            user = User.objects.create_user(
                username=login_username,
                email=employee.email or '',
                password=login_password,
                first_name=employee.name
            )

            UserProfile.objects.create(
                user=user,
                business=employee.business,
                role='Employee',
                phone=employee.phone
            )

            employee.user = user

        employee.save()

        log_activity(request.user, f'Updated employee {employee.name}', 'Employees')
        messages.success(request, 'Employee updated successfully.')
        return redirect('/employees/')

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Edit Employee',
        'employee': employee
    })


@admin_required
def employee_delete(request, pk):
    employee = get_object_or_404(get_employee_queryset(request), pk=pk)

    if request.method == 'POST':
        name = employee.name
        employee.delete()

        log_activity(request.user, f'Deleted employee {name}', 'Employees')
        messages.success(request, 'Employee deleted successfully.')
        return redirect('/employees/')

    return render(request, 'employees/delete_employee.html', {
        'employee': employee
    })