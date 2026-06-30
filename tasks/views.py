from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required
from activity_logs.utils import log_activity
from businesses.utils import get_current_business

from .forms import TaskForm
from .models import Task


def get_task_queryset(request):
    business = get_current_business(request)

    if request.user.is_superuser and business is None:
        return Task.objects.select_related('business', 'assigned_to').all()

    return Task.objects.select_related('business', 'assigned_to').filter(business=business)


@admin_required
def task_list(request):
    tasks = get_task_queryset(request)

    q = request.GET.get('q')
    if q:
        tasks = tasks.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(priority__icontains=q) |
            Q(status__icontains=q) |
            Q(assigned_to__name__icontains=q)
        )

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks
    })


@admin_required
def task_add(request):
    business = get_current_business(request)

    form = TaskForm(request.POST or None, business=business)

    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.business = business
        task.save()

        log_activity(request.user, f'Added task {task.title}', 'Tasks')
        messages.success(request, 'Task added successfully.')
        return redirect('/tasks/')

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Add Task'
    })


@admin_required
def task_edit(request, pk):
    business = get_current_business(request)
    task = get_object_or_404(get_task_queryset(request), pk=pk)

    form = TaskForm(request.POST or None, instance=task, business=business)

    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.business = task.business or business
        task.save()

        log_activity(request.user, f'Updated task {task.title}', 'Tasks')
        messages.success(request, 'Task updated successfully.')
        return redirect('/tasks/')

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Edit Task',
        'task': task
    })


@admin_required
def task_delete(request, pk):
    task = get_object_or_404(get_task_queryset(request), pk=pk)

    if request.method == 'POST':
        title = task.title
        task.delete()

        log_activity(request.user, f'Deleted task {title}', 'Tasks')
        messages.success(request, 'Task deleted successfully.')
        return redirect('/tasks/')

    return render(request, 'tasks/delete_task.html', {
        'task': task
    })