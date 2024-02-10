from django import forms
from .models import Zadanie

class ZadanieForm(forms.ModelForm):
    class Meta:
        model = Zadanie
        fields = ['description', 'comments', 'status', 'deadline', 'assigned_to', 'task_photo', 'signature_image']
