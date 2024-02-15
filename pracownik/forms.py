from django import forms
from .models import Task, TaskAssignment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'due_date', 'photo', 'status']
