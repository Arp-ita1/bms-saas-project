from django import forms
from django.contrib.auth.models import User

from .models import Employee


class EmployeeForm(forms.ModelForm):
    create_login_account = forms.BooleanField(
        required=False,
        label='Create employee login account'
    )

    login_username = forms.CharField(
        required=False,
        label='Login Username'
    )

    login_password = forms.CharField(
        required=False,
        label='Login Password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = Employee
        fields = [
            'name',
            'email',
            'phone',
            'position',
            'salary',
            'joining_date',
            'address',
            'status',
        ]

        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()

        create_login_account = cleaned_data.get('create_login_account')
        login_username = cleaned_data.get('login_username')
        login_password = cleaned_data.get('login_password')

        if create_login_account:
            if self.instance and self.instance.pk and self.instance.user:
                raise forms.ValidationError(
                    'This employee already has a login account.'
                )

            if not login_username:
                self.add_error('login_username', 'Username is required.')

            if not login_password:
                self.add_error('login_password', 'Password is required.')

            if login_username and User.objects.filter(username=login_username).exists():
                self.add_error('login_username', 'This username already exists.')

        return cleaned_data