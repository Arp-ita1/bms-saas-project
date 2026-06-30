from django.urls import path
from . import views

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('add/', views.invoice_add, name='invoice_add'),
    path('edit/<int:pk>/', views.invoice_edit, name='invoice_edit'),
    path('delete/<int:pk>/', views.invoice_delete, name='invoice_delete'),
    path('detail/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('print/<int:pk>/', views.invoice_print, name='invoice_print'),
]
