from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.business_register, name='business_register'),

    path('../platform/', views.platform_dashboard, name='platform_dashboard'),
    path('../platform/businesses/', views.platform_business_list, name='platform_business_list'),
    path('../platform/businesses/<int:pk>/', views.platform_business_detail, name='platform_business_detail'),
    path('../platform/subscriptions/', views.platform_subscription_list, name='platform_subscription_list'),
    path('../platform/plans/', views.platform_plan_list, name='platform_plan_list'),
]