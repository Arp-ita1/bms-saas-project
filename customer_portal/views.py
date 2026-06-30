from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from customers.models import Customer
from orders.models import Order
from invoices.models import Invoice


def customer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')

        try:
            profile = request.user.profile
        except Exception:
            profile = None

        if profile and profile.role == 'Customer':
            return view_func(request, *args, **kwargs)

        if profile and profile.role == 'BusinessAdmin':
            return redirect('/dashboard/')

        if profile and profile.role == 'Employee':
            return redirect('/employee-portal/')

        if request.user.is_superuser or request.user.is_staff:
            return redirect('/platform/')

        return redirect('/accounts/login/')

    return wrapper


def get_customer(request):
    customer = Customer.objects.filter(user=request.user).select_related('business').first()

    if not customer and request.user.email:
        customer = Customer.objects.filter(email=request.user.email).select_related('business').first()

    return customer


@login_required
@customer_required
def customer_dashboard(request):
    customer = get_customer(request)

    if customer:
        business = customer.business
        orders = Order.objects.filter(customer=customer, business=business)
        invoices = Invoice.objects.filter(customer=customer, business=business)
    else:
        business = None
        orders = Order.objects.none()
        invoices = Invoice.objects.none()

    total_invoice_amount = 0
    total_paid_amount = 0
    total_pending_amount = 0

    for invoice in invoices:
        total_invoice_amount += invoice.total_amount or 0
        total_paid_amount += invoice.paid_amount or 0
        total_pending_amount += invoice.pending_amount or 0

    context = {
        'customer': customer,
        'business': business,

        'total_orders': orders.count(),
        'pending_orders': orders.filter(status='Pending').count(),
        'completed_orders': orders.filter(status='Completed').count(),

        'total_invoices': invoices.count(),
        'paid_invoices': invoices.filter(status='Paid').count(),
        'unpaid_invoices': invoices.filter(status='Unpaid').count(),

        'total_invoice_amount': total_invoice_amount,
        'total_paid_amount': total_paid_amount,
        'total_pending_amount': total_pending_amount,

        'recent_orders': orders[:5],
        'recent_invoices': invoices[:5],
    }

    return render(request, 'customer_portal/customer_dashboard.html', context)


@login_required
@customer_required
def customer_orders(request):
    customer = get_customer(request)

    if customer:
        orders = Order.objects.filter(customer=customer, business=customer.business)
    else:
        orders = Order.objects.none()

    q = request.GET.get('q')
    status = request.GET.get('status')

    if q:
        orders = orders.filter(title__icontains=q)

    if status:
        orders = orders.filter(status=status)

    return render(request, 'customer_portal/customer_orders.html', {
        'customer': customer,
        'business': customer.business if customer else None,
        'orders': orders,
        'q': q,
        'status': status,
    })


@login_required
@customer_required
def customer_order_detail(request, pk):
    customer = get_customer(request)

    order = get_object_or_404(
        Order,
        pk=pk,
        customer=customer,
        business=customer.business
    )

    return render(request, 'customer_portal/customer_order_detail.html', {
        'customer': customer,
        'business': customer.business,
        'order': order,
    })


@login_required
@customer_required
def customer_invoices(request):
    customer = get_customer(request)

    if customer:
        invoices = Invoice.objects.filter(customer=customer, business=customer.business)
    else:
        invoices = Invoice.objects.none()

    q = request.GET.get('q')
    status = request.GET.get('status')

    if q:
        invoices = invoices.filter(invoice_number__icontains=q)

    if status:
        invoices = invoices.filter(status=status)

    return render(request, 'customer_portal/customer_invoices.html', {
        'customer': customer,
        'business': customer.business if customer else None,
        'invoices': invoices,
        'q': q,
        'status': status,
    })


@login_required
@customer_required
def customer_invoice_detail(request, pk):
    customer = get_customer(request)

    invoice = get_object_or_404(
        Invoice,
        pk=pk,
        customer=customer,
        business=customer.business
    )

    return render(request, 'customer_portal/customer_invoice_detail.html', {
        'customer': customer,
        'business': customer.business,
        'invoice': invoice,
    })


@login_required
@customer_required
def customer_profile(request):
    customer = get_customer(request)

    return render(request, 'customer_portal/customer_profile.html', {
        'customer': customer,
        'business': customer.business if customer else None,
    })