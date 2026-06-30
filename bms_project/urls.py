from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from businesses import views as business_views
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),

    path('customers/', include('customers.urls')),
    path('employees/', include('employees.urls')),
    path('tasks/', include('tasks.urls')),
    path('appointments/', include('appointments.urls')),
    path('orders/', include('orders.urls')),
    path('invoices/', include('invoices.urls')),
    path('notifications/', include('notifications.urls')),
    path('business-settings/', include('business_settings.urls')),
    path('customer-portal/', include('customer_portal.urls')),

    path('business/', include('businesses.urls')),

    path('platform/', business_views.platform_dashboard, name='platform_dashboard'),
    path('platform/businesses/', business_views.platform_business_list, name='platform_business_list'),
    path('platform/businesses/<int:pk>/', business_views.platform_business_detail, name='platform_business_detail'),
    path('platform/subscriptions/', business_views.platform_subscription_list, name='platform_subscription_list'),
    path('platform/plans/', business_views.platform_plan_list, name='platform_plan_list'),
    path('employee-portal/', include('employee_portal.urls')),
    path('cutomer-portal/', lambda request: redirect('/customer-portal/')),

    path('search/', dashboard_views.global_search, name='global_search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)