from django import forms

from customers.models import Customer
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer',
            'title',
            'total_amount',
            'status',
            'order_date',
            'description',
        ]

        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        business = kwargs.pop('business', None)
        super().__init__(*args, **kwargs)

        if business:
            self.fields['customer'].queryset = Customer.objects.filter(
                business=business,
                status='Active'
            )
        else:
            self.fields['customer'].queryset = Customer.objects.none()

        self.fields['customer'].empty_label = 'Select Customer'