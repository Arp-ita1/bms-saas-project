from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required
from .models import Lead


@admin_required
def lead_list(request):
    leads = Lead.objects.all()

    q = request.GET.get('q')
    status = request.GET.get('status')

    if q:
        leads = leads.filter(
            Q(name__icontains=q) |
            Q(business_name__icontains=q) |
            Q(email__icontains=q) |
            Q(phone__icontains=q) |
            Q(inquiry_type__icontains=q) |
            Q(preferred_plan__icontains=q)
        )

    if status:
        leads = leads.filter(status=status)

    return render(request, 'leads/lead_list.html', {
        'leads': leads,
        'status': status,
    })


@admin_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == 'POST':
        lead.status = request.POST.get('status')
        lead.admin_note = request.POST.get('admin_note')
        lead.save()

        messages.success(request, 'Inquiry updated successfully.')
        return redirect('/leads/')

    return render(request, 'leads/lead_detail.html', {
        'lead': lead,
    })


@admin_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == 'POST':
        lead.delete()
        messages.success(request, 'Inquiry deleted successfully.')
        return redirect('/leads/')

    return render(request, 'leads/lead_delete.html', {
        'lead': lead,
    })