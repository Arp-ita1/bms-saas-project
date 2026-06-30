from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required
from activity_logs.utils import log_activity
from businesses.utils import get_current_business

from .forms import NotificationForm
from .models import Notification


def get_notification_queryset(request):
    business = get_current_business(request)

    if request.user.is_superuser and business is None:
        return Notification.objects.select_related('user', 'customer').all()

    return Notification.objects.select_related('user', 'customer').filter(business=business)


@admin_required
def notification_list(request):
    notifications = get_notification_queryset(request)

    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications
    })


@admin_required
def notification_add(request):
    business = get_current_business(request)
    form = NotificationForm(request.POST or None, business=business)

    if request.method == 'POST' and form.is_valid():
        notification = form.save(commit=False)
        notification.business = business

        if notification.customer and not notification.user:
            notification.user = notification.customer.user

        notification.save()

        log_activity(request.user, f'Added notification {notification.title}', 'Notifications')
        messages.success(request, 'Notification added successfully.')
        return redirect('/notifications/')

    return render(request, 'notifications/notification_form.html', {
        'form': form,
        'title': 'Add Notification'
    })


@admin_required
def notification_delete(request, pk):
    notification = get_object_or_404(get_notification_queryset(request), pk=pk)

    if request.method == 'POST':
        title = notification.title
        notification.delete()

        log_activity(request.user, f'Deleted notification {title}', 'Notifications')
        messages.success(request, 'Notification deleted successfully.')
        return redirect('/notifications/')

    return render(request, 'notifications/delete_notification.html', {
        'notification': notification
    })