from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('detail/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('delete/<int:pk>/', views.lead_delete, name='lead_delete'),
]