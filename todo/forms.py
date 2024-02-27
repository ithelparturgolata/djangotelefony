from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'comments', 'status', 'deadline', 'assigned_to', 'task_photo', 'signature_image']
