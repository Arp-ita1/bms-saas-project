from django.urls import path

from . import views

urlpatterns = [
    path('', views.customer_dashboard, name='customer_dashboard'),
    path('orders/', views.customer_orders, name='customer_orders'),
    path('orders/<int:pk>/', views.customer_order_detail, name='customer_order_detail'),
    path('invoices/', views.customer_invoices, name='customer_invoices'),
    path('invoices/<int:pk>/', views.customer_invoice_detail, name='customer_invoice_detail'),
    path('profile/', views.customer_profile, name='customer_profile'),
]