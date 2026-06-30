from django import forms

from .models import BusinessProfile


class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = [
            'company_name',
            'owner_name',
            'email',
            'phone',
            'address',
            'city',
            'state',
            'logo',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }