from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required
from activity_logs.utils import log_activity
from businesses.utils import get_current_business

from .forms import AppointmentForm
from .models import Appointment


def get_appointment_queryset(request):
    business = get_current_business(request)

    if request.user.is_superuser and business is None:
        return Appointment.objects.select_related('customer').all()

    return Appointment.objects.select_related('customer').filter(business=business)


@admin_required
def appointment_list(request):
    appointments = get_appointment_queryset(request)

    q = request.GET.get('q')
    if q:
        appointments = appointments.filter(
            Q(title__icontains=q) |
            Q(customer__name__icontains=q) |
            Q(status__icontains=q)
        )

    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments
    })


@admin_required
def appointment_add(request):
    business = get_current_business(request)
    form = AppointmentForm(request.POST or None, business=business)

    if request.method == 'POST' and form.is_valid():
        appointment = form.save(commit=False)
        appointment.business = business
        appointment.save()

        log_activity(request.user, f'Added appointment {appointment.title}', 'Appointments')
        messages.success(request, 'Appointment added successfully.')
        return redirect('/appointments/')

    return render(request, 'appointments/appointment_form.html', {
        'form': form,
        'title': 'Add Appointment'
    })


@admin_required
def appointment_edit(request, pk):
    business = get_current_business(request)
    appointment = get_object_or_404(get_appointment_queryset(request), pk=pk)

    form = AppointmentForm(request.POST or None, instance=appointment, business=business)

    if request.method == 'POST' and form.is_valid():
        appointment = form.save(commit=False)
        appointment.business = appointment.business or business
        appointment.save()

        log_activity(request.user, f'Updated appointment {appointment.title}', 'Appointments')
        messages.success(request, 'Appointment updated successfully.')
        return redirect('/appointments/')

    return render(request, 'appointments/appointment_form.html', {
        'form': form,
        'title': 'Edit Appointment'
    })


@admin_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(get_appointment_queryset(request), pk=pk)

    if request.method == 'POST':
        title = appointment.title
        appointment.delete()

        log_activity(request.user, f'Deleted appointment {title}', 'Appointments')
        messages.success(request, 'Appointment deleted successfully.')
        return redirect('/appointments/')

    return render(request, 'appointments/delete_appointment.html', {
        'appointment': appointment
    })