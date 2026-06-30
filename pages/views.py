from django.contrib import messages
from django.shortcuts import redirect, render

from leads.models import Lead


def home(request):
    return render(request, 'pages/home.html')


def features(request):
    return render(request, 'pages/features.html')


def modules(request):
    return render(request, 'pages/modules.html')


def pricing(request):
    return render(request, 'pages/pricing.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        inquiry_type = request.POST.get('service')
        preferred_plan = request.POST.get('preferred_plan')
        message = request.POST.get('message')

        Lead.objects.create(
            name=name,
            business_name=business_name,
            email=email,
            phone=phone,
            inquiry_type=inquiry_type,
            preferred_plan=preferred_plan,
            message=message,
        )

        messages.success(
            request,
            'Your BMS inquiry has been submitted successfully. Our team will contact you soon.'
        )
        return redirect('/contact/')

    return render(request, 'pages/contact.html')