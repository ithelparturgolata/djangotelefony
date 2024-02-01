from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['employee', 'description', 'status', 'comments', 'date_added', 'due_date']