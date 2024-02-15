from django import forms
from .models import Contract

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['contractor', 'file', 'description', 'start_date', 'end_date']
        labels = {'contractor': 'Wykonawca', 'file': 'Plik', 'description': 'Opis', 'start_date': 'Umowa od', 'end_date': 'Umowa do'}