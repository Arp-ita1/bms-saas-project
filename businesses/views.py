from django.apps import apps
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Business, Plan, Subscription, UserProfile
from .utils import super_admin_required


def business_register(request):
    selected_plan = request.GET.get('plan', 'Basic Plan')
    selected_plan_obj = Plan.objects.filter(name=selected_plan, is_active=True).first()

    if request.method == 'POST':
        owner_name = request.POST.get('owner_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        business_name = request.POST.get('business_name')
        business_type = request.POST.get('business_type')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        plan_id = request.POST.get('plan_id')

        plan = Plan.objects.filter(id=plan_id, is_active=True).first()

        if not plan:
            messages.error(request, 'Please select a valid plan.')
            return redirect(request.path)

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect(request.path)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect(request.path)

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect(request.path)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=owner_name
        )

        business = Business.objects.create(
            owner=user,
            business_name=business_name,
            business_type=business_type,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            status='Active'
        )

        UserProfile.objects.create(
            user=user,
            business=business,
            role='BusinessAdmin',
            phone=phone
        )

        Subscription.objects.create(
            business=business,
            plan=plan,
            status='Trial',
            payment_status='Pending'
        )

        login(request, user)

        messages.success(request, 'Business account created successfully.')
        return redirect('/dashboard/')

    plans = Plan.objects.filter(is_active=True)

    return render(request, 'businesses/business_register.html', {
        'plans': plans,
        'selected_plan': selected_plan,
        'selected_plan_obj': selected_plan_obj,
    })


@super_admin_required
def platform_dashboard(request):
    businesses = Business.objects.all()
    subscriptions = Subscription.objects.select_related('business', 'plan').all()
    plans = Plan.objects.all()

    paid_subscriptions = subscriptions.filter(payment_status='Paid')
    total_revenue = sum(
        subscription.plan.price for subscription in paid_subscriptions if subscription.plan
    )

    leads_count = 0
    recent_leads = []

    if apps.is_installed('leads'):
        Lead = apps.get_model('leads', 'Lead')
        leads_count = Lead.objects.count()
        recent_leads = Lead.objects.all()[:5]

    context = {
        'total_businesses': businesses.count(),
        'active_businesses': businesses.filter(status='Active').count(),
        'inactive_businesses': businesses.exclude(status='Active').count(),

        'total_plans': plans.count(),
        'active_plans': plans.filter(is_active=True).count(),

        'total_subscriptions': subscriptions.count(),
        'trial_subscriptions': subscriptions.filter(status='Trial').count(),
        'active_subscriptions': subscriptions.filter(status='Active').count(),
        'expired_subscriptions': subscriptions.filter(status='Expired').count(),

        'paid_subscriptions': subscriptions.filter(payment_status='Paid').count(),
        'pending_payments': subscriptions.filter(payment_status='Pending').count(),

        'total_revenue': total_revenue,

        'leads_count': leads_count,
        'recent_leads': recent_leads,

        'recent_businesses': businesses[:6],
        'recent_subscriptions': subscriptions[:6],
    }

    return render(request, 'businesses/platform_dashboard.html', context)


@super_admin_required
def platform_business_list(request):
    businesses = Business.objects.select_related('owner').all()

    q = request.GET.get('q')
    status = request.GET.get('status')

    if q:
        businesses = businesses.filter(
            Q(business_name__icontains=q) |
            Q(owner__username__icontains=q) |
            Q(email__icontains=q) |
            Q(phone__icontains=q) |
            Q(business_type__icontains=q)
        )

    if status:
        businesses = businesses.filter(status=status)

    return render(request, 'businesses/platform_business_list.html', {
        'businesses': businesses,
        'status': status,
    })


@super_admin_required
def platform_business_detail(request, pk):
    business = get_object_or_404(Business, pk=pk)
    subscription = Subscription.objects.filter(business=business).select_related('plan').first()

    if request.method == 'POST':
        business.status = request.POST.get('business_status')
        business.save()

        if subscription:
            subscription.status = request.POST.get('subscription_status')
            subscription.payment_status = request.POST.get('payment_status')
            subscription.save()

        messages.success(request, 'Business and subscription updated successfully.')
        return redirect('/platform/businesses/')

    return render(request, 'businesses/platform_business_detail.html', {
        'business': business,
        'subscription': subscription,
    })


@super_admin_required
def platform_subscription_list(request):
    subscriptions = Subscription.objects.select_related('business', 'plan').all()

    q = request.GET.get('q')
    status = request.GET.get('status')
    payment_status = request.GET.get('payment_status')

    if q:
        subscriptions = subscriptions.filter(
            Q(business__business_name__icontains=q) |
            Q(plan__name__icontains=q) |
            Q(business__owner__username__icontains=q)
        )

    if status:
        subscriptions = subscriptions.filter(status=status)

    if payment_status:
        subscriptions = subscriptions.filter(payment_status=payment_status)

    return render(request, 'businesses/platform_subscription_list.html', {
        'subscriptions': subscriptions,
        'status': status,
        'payment_status': payment_status,
    })


@super_admin_required
def platform_plan_list(request):
    plans = Plan.objects.all()

    return render(request, 'businesses/platform_plan_list.html', {
        'plans': plans,
    })