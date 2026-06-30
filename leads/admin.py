from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'business_name',
        'email',
        'phone',
        'inquiry_type',
        'preferred_plan',
        'status',
        'created_at',
    ]

    search_fields = [
        'name',
        'business_name',
        'email',
        'phone',
        'inquiry_type',
        'preferred_plan',
    ]

    list_filter = [
        'inquiry_type',
        'preferred_plan',
        'status',
        'created_at',
    ]