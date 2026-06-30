from django.urls import path
from .views import settings_page

urlpatterns = [
    path('', settings_page, name='business_settings'),
]
