from django import forms
from django.contrib.auth.models import User

from customers.models import Customer
from .models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = [
            'user',
            'customer',
            'title',
            'message',
            'is_read',
        ]

        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, business=None, **kwargs):
        super().__init__(*args, **kwargs)

        if business:
            self.fields['customer'].queryset = Customer.objects.filter(business=business)
            self.fields['user'].queryset = User.objects.filter(profile__business=business)
        else:
            self.fields['customer'].queryset = Customer.objects.all()
            self.fields['user'].queryset = User.objects.all()