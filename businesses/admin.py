from django.contrib import admin

from .models import Business, Plan, Subscription, UserProfile


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'duration_days',
        'max_customers',
        'max_employees',
        'max_invoices',
        'is_active',
    ]
    search_fields = ['name']
    list_filter = ['is_active']


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = [
        'business_name',
        'owner',
        'email',
        'phone',
        'status',
        'created_at',
    ]
    search_fields = [
        'business_name',
        'owner__username',
        'email',
        'phone',
    ]
    list_filter = ['status', 'created_at']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'business',
        'plan',
        'start_date',
        'end_date',
        'status',
        'payment_status',
    ]
    search_fields = [
        'business__business_name',
        'plan__name',
    ]
    list_filter = [
        'status',
        'payment_status',
    ]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'business',
        'role',
        'phone',
        'created_at',
    ]
    search_fields = [
        'user__username',
        'business__business_name',
        'phone',
    ]
    list_filter = ['role']