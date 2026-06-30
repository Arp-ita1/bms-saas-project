from django import forms

from customers.models import Customer
from orders.models import Order
from .models import Invoice, InvoiceItem


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'customer',
            'order',
            'description',
            'invoice_date',
            'due_date',
            'subtotal',
            'tax',
            'discount',
            'total_amount',
            'paid_amount',
            'status',
            'notes',
        ]

        widgets = {
            'invoice_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, business=None, **kwargs):
        super().__init__(*args, **kwargs)

        if business:
            self.fields['customer'].queryset = Customer.objects.filter(business=business)
            self.fields['order'].queryset = Order.objects.filter(business=business)
        else:
            self.fields['customer'].queryset = Customer.objects.all()
            self.fields['order'].queryset = Order.objects.all()


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = [
            'item_name',
            'quantity',
            'price',
        ]