from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required
from activity_logs.utils import log_activity
from business_settings.models import BusinessProfile
from businesses.utils import get_current_business

from .forms import InvoiceForm, InvoiceItemForm
from .models import Invoice


def get_invoice_queryset(request):
    business = get_current_business(request)

    if request.user.is_superuser and business is None:
        return Invoice.objects.select_related('customer', 'order').all()

    return Invoice.objects.select_related('customer', 'order').filter(business=business)


@admin_required
def invoice_list(request):
    invoices = get_invoice_queryset(request)

    q = request.GET.get('q')
    if q:
        invoices = invoices.filter(
            Q(invoice_number__icontains=q) |
            Q(customer__name__icontains=q) |
            Q(status__icontains=q)
        )

    return render(request, 'invoices/invoice_list.html', {
        'invoices': invoices
    })


@admin_required
def invoice_add(request):
    business = get_current_business(request)
    form = InvoiceForm(request.POST or None, business=business)

    if request.method == 'POST' and form.is_valid():
        invoice = form.save(commit=False)
        invoice.business = business
        invoice.save()

        log_activity(request.user, f'Added invoice {invoice.invoice_number}', 'Invoices')
        messages.success(request, 'Invoice added successfully.')
        return redirect('/invoices/detail/{}/'.format(invoice.id))

    return render(request, 'invoices/invoice_form.html', {
        'form': form,
        'title': 'Add Invoice'
    })


@admin_required
def invoice_edit(request, pk):
    business = get_current_business(request)
    invoice = get_object_or_404(get_invoice_queryset(request), pk=pk)

    form = InvoiceForm(request.POST or None, instance=invoice, business=business)

    if request.method == 'POST' and form.is_valid():
        invoice = form.save(commit=False)
        invoice.business = invoice.business or business
        invoice.save()

        log_activity(request.user, f'Updated invoice {invoice.invoice_number}', 'Invoices')
        messages.success(request, 'Invoice updated successfully.')
        return redirect('/invoices/detail/{}/'.format(invoice.id))

    return render(request, 'invoices/invoice_form.html', {
        'form': form,
        'title': 'Edit Invoice'
    })


@admin_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(get_invoice_queryset(request), pk=pk)

    if request.method == 'POST':
        number = invoice.invoice_number
        invoice.delete()

        log_activity(request.user, f'Deleted invoice {number}', 'Invoices')
        messages.success(request, 'Invoice deleted successfully.')
        return redirect('/invoices/')

    return render(request, 'invoices/delete_invoice.html', {
        'invoice': invoice
    })


@admin_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(get_invoice_queryset(request), pk=pk)

    item_form = InvoiceItemForm(request.POST or None)

    if request.method == 'POST' and item_form.is_valid():
        item = item_form.save(commit=False)
        item.invoice = invoice
        item.save()

        messages.success(request, 'Invoice item added successfully.')
        return redirect('/invoices/detail/{}/'.format(invoice.id))

    business = BusinessProfile.get_profile(get_current_business(request))

    return render(request, 'invoices/invoice_detail.html', {
        'invoice': invoice,
        'business': business,
        'item_form': item_form,
    })


@admin_required
def invoice_print(request, pk):
    invoice = get_object_or_404(get_invoice_queryset(request), pk=pk)
    business = BusinessProfile.get_profile(get_current_business(request))

    return render(request, 'invoices/invoice_print.html', {
        'invoice': invoice,
        'business': business
    })