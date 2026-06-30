from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required
from activity_logs.utils import log_activity
from businesses.models import UserProfile
from businesses.utils import get_current_business

from .forms import CustomerForm
from .models import Customer


def get_customer_queryset(request):
    business = get_current_business(request)

    if request.user.is_superuser and business is None:
        return Customer.objects.select_related('user', 'business').all()

    return Customer.objects.select_related('user', 'business').filter(business=business)


@admin_required
def customer_list(request):
    customers = get_customer_queryset(request)

    q = request.GET.get('q')
    if q:
        customers = customers.filter(
            Q(name__icontains=q) |
            Q(email__icontains=q) |
            Q(phone__icontains=q) |
            Q(company_name__icontains=q) |
            Q(city__icontains=q)
        )

    return render(request, 'customers/customer_list.html', {
        'customers': customers
    })


@admin_required
def customer_add(request):
    business = get_current_business(request)
    form = CustomerForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        customer = form.save(commit=False)
        customer.business = business

        create_portal_account = form.cleaned_data.get('create_portal_account')
        portal_username = form.cleaned_data.get('portal_username')
        portal_password = form.cleaned_data.get('portal_password')

        if create_portal_account:
            user = User.objects.create_user(
                username=portal_username,
                email=customer.email or '',
                password=portal_password,
                first_name=customer.name
            )

            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'business': business,
                    'role': 'Customer',
                    'phone': customer.phone
                }
            )

            customer.user = user

        customer.save()

        log_activity(request.user, f'Added customer {customer.name}', 'Customers')
        messages.success(request, 'Customer added successfully.')
        return redirect('/customers/')

    return render(request, 'customers/customer_form.html', {
        'form': form,
        'title': 'Add Customer'
    })


@admin_required
def customer_edit(request, pk):
    customer = get_object_or_404(get_customer_queryset(request), pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)

    if request.method == 'POST' and form.is_valid():
        customer = form.save(commit=False)
        customer.business = customer.business or get_current_business(request)

        create_portal_account = form.cleaned_data.get('create_portal_account')
        portal_username = form.cleaned_data.get('portal_username')
        portal_password = form.cleaned_data.get('portal_password')

        if create_portal_account and not customer.user:
            user = User.objects.create_user(
                username=portal_username,
                email=customer.email or '',
                password=portal_password,
                first_name=customer.name
            )

            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'business': customer.business,
                    'role': 'Customer',
                    'phone': customer.phone
                }
            )

            customer.user = user

        customer.save()

        log_activity(request.user, f'Updated customer {customer.name}', 'Customers')
        messages.success(request, 'Customer updated successfully.')
        return redirect('/customers/')

    return render(request, 'customers/customer_form.html', {
        'form': form,
        'title': 'Edit Customer',
        'customer': customer
    })


@admin_required
def customer_delete(request, pk):
    customer = get_object_or_404(get_customer_queryset(request), pk=pk)

    if request.method == 'POST':
        name = customer.name
        customer.delete()

        log_activity(request.user, f'Deleted customer {name}', 'Customers')
        messages.success(request, 'Customer deleted successfully.')
        return redirect('/customers/')

    return render(request, 'customers/delete_customer.html', {
        'customer': customer
    })