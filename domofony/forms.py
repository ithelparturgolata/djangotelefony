from django import forms
from .models import TaskIntercom


class TaskFormIntercom(forms.ModelForm):
    class Meta:
        model = TaskIntercom
        fields = ['user', 'description', 'estate', 'street', 'contractor', 'status', 'planned_execution_date']
