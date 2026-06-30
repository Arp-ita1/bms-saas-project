from django.urls import path

from . import views

urlpatterns = [
    path('', views.employee_dashboard, name='employee_dashboard'),
    path('tasks/', views.employee_tasks, name='employee_tasks'),
    path('tasks/<int:pk>/', views.employee_task_detail, name='employee_task_detail'),
    path('profile/', views.employee_profile, name='employee_profile'),
]