from django import forms

from employees.models import Employee
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'assigned_to',
            'priority',
            'status',
            'due_date',
            'description',
        ]

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        business = kwargs.pop('business', None)
        super().__init__(*args, **kwargs)

        if business:
            self.fields['assigned_to'].queryset = Employee.objects.filter(
                business=business,
                status='Active'
            )
        else:
            self.fields['assigned_to'].queryset = Employee.objects.none()

        self.fields['assigned_to'].empty_label = 'Select Employee'