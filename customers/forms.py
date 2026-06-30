from django import forms
from django.contrib.auth.models import User

from .models import Customer


class CustomerForm(forms.ModelForm):
    create_portal_account = forms.BooleanField(
        required=False,
        label='Create customer portal login account'
    )

    portal_username = forms.CharField(
        required=False,
        label='Portal Username'
    )

    portal_password = forms.CharField(
        required=False,
        label='Portal Password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = Customer
        fields = [
            'name',
            'email',
            'phone',
            'company_name',
            'address',
            'city',
            'state',
            'status',
        ]

        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()

        create_portal_account = cleaned_data.get('create_portal_account')
        portal_username = cleaned_data.get('portal_username')
        portal_password = cleaned_data.get('portal_password')

        if create_portal_account:
            if self.instance and self.instance.pk and self.instance.user:
                raise forms.ValidationError(
                    'This customer already has a portal account.'
                )

            if not portal_username:
                self.add_error('portal_username', 'Username is required.')

            if not portal_password:
                self.add_error('portal_password', 'Password is required.')

            if portal_username and User.objects.filter(username=portal_username).exists():
                self.add_error('portal_username', 'This username already exists.')

        return cleaned_data