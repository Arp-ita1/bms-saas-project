from django import forms

from customers.models import Customer
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'customer',
            'title',
            'date',
            'time',
            'notes',
            'status',
        ]

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, business=None, **kwargs):
        super().__init__(*args, **kwargs)

        if business:
            self.fields['customer'].queryset = Customer.objects.filter(business=business)
        else:
            self.fields['customer'].queryset = Customer.objects.all()