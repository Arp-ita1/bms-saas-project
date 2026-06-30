from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from employees.models import Employee
from tasks.models import Task


def employee_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')

        try:
            profile = request.user.profile
        except Exception:
            profile = None

        if profile and profile.role == 'Employee':
            return view_func(request, *args, **kwargs)

        if profile and profile.role == 'BusinessAdmin':
            return redirect('/dashboard/')

        if profile and profile.role == 'Customer':
            return redirect('/customer-portal/')

        if request.user.is_superuser or request.user.is_staff:
            return redirect('/platform/')

        return redirect('/accounts/login/')

    return wrapper


def get_employee(request):
    employee = Employee.objects.filter(user=request.user).select_related('business').first()

    if not employee and request.user.email:
        employee = Employee.objects.filter(email=request.user.email).select_related('business').first()

    return employee


@login_required
@employee_required
def employee_dashboard(request):
    employee = get_employee(request)

    if employee:
        business = employee.business
        tasks = Task.objects.filter(
            business=business,
            assigned_to=employee
        ).select_related('assigned_to')
    else:
        business = None
        tasks = Task.objects.none()

    context = {
        'employee': employee,
        'business': business,

        'total_tasks': tasks.count(),
        'pending_tasks': tasks.filter(status='Pending').count(),
        'in_progress_tasks': tasks.filter(status='In Progress').count(),
        'completed_tasks': tasks.filter(status='Completed').count(),

        'high_priority_tasks': tasks.filter(priority='High').count(),
        'recent_tasks': tasks[:6],
    }

    return render(request, 'employee_portal/employee_dashboard.html', context)


@login_required
@employee_required
def employee_tasks(request):
    employee = get_employee(request)

    if employee:
        tasks = Task.objects.filter(
            business=employee.business,
            assigned_to=employee
        )
    else:
        tasks = Task.objects.none()

    q = request.GET.get('q')
    status = request.GET.get('status')
    priority = request.GET.get('priority')

    if q:
        tasks = tasks.filter(title__icontains=q)

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    return render(request, 'employee_portal/employee_tasks.html', {
        'employee': employee,
        'business': employee.business if employee else None,
        'tasks': tasks,
        'q': q,
        'status': status,
        'priority': priority,
    })


@login_required
@employee_required
def employee_task_detail(request, pk):
    employee = get_employee(request)

    task = get_object_or_404(
        Task,
        pk=pk,
        assigned_to=employee,
        business=employee.business
    )

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status in ['Pending', 'In Progress', 'Completed']:
            task.status = new_status
            task.save()
            messages.success(request, 'Task status updated successfully.')

        return redirect('/employee-portal/tasks/')

    return render(request, 'employee_portal/employee_task_detail.html', {
        'employee': employee,
        'business': employee.business,
        'task': task,
    })


@login_required
@employee_required
def employee_profile(request):
    employee = get_employee(request)

    return render(request, 'employee_portal/employee_profile.html', {
        'employee': employee,
        'business': employee.business if employee else None,
    })