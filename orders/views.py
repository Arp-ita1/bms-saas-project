from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required
from activity_logs.utils import log_activity
from businesses.utils import get_current_business

from .forms import OrderForm
from .models import Order


def get_order_queryset(request):
    business = get_current_business(request)

    if request.user.is_superuser and business is None:
        return Order.objects.select_related('business', 'customer').all()

    return Order.objects.select_related('business', 'customer').filter(business=business)


@admin_required
def order_list(request):
    orders = get_order_queryset(request)

    q = request.GET.get('q')
    if q:
        orders = orders.filter(
            Q(order_number__icontains=q) |
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(status__icontains=q) |
            Q(customer__name__icontains=q) |
            Q(customer__phone__icontains=q)
        )

    return render(request, 'orders/order_list.html', {
        'orders': orders
    })


@admin_required
def order_add(request):
    business = get_current_business(request)
    form = OrderForm(request.POST or None, business=business)

    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        order.business = business
        order.save()

        log_activity(request.user, f'Added order {order.order_number}', 'Orders')
        messages.success(request, 'Order added successfully.')
        return redirect('/orders/')

    return render(request, 'orders/order_form.html', {
        'form': form,
        'title': 'Add Order'
    })


@admin_required
def order_edit(request, pk):
    business = get_current_business(request)
    order = get_object_or_404(get_order_queryset(request), pk=pk)

    form = OrderForm(request.POST or None, instance=order, business=business)

    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        order.business = order.business or business
        order.save()

        log_activity(request.user, f'Updated order {order.order_number}', 'Orders')
        messages.success(request, 'Order updated successfully.')
        return redirect('/orders/')

    return render(request, 'orders/order_form.html', {
        'form': form,
        'title': 'Edit Order',
        'order': order
    })


@admin_required
def order_delete(request, pk):
    order = get_object_or_404(get_order_queryset(request), pk=pk)

    if request.method == 'POST':
        order_number = order.order_number
        order.delete()

        log_activity(request.user, f'Deleted order {order_number}', 'Orders')
        messages.success(request, 'Order deleted successfully.')
        return redirect('/orders/')

    return render(request, 'orders/delete_order.html', {
        'order': order
    })