from django import forms
from .models import Contract, ContractFile, Contractor


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['contractor', 'description', 'start_date', 'end_date']
        labels = {'contractor': 'Wykonawca', 'files': 'Pliki', 'description': 'Opis', 'start_date': 'Umowa od', 'end_date': 'Umowa do'}
        

class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = ['name']
        labels = {'name': 'Wykonawca'}


class ContractFileForm(forms.ModelForm):
    class Meta:
        model = ContractFile
        fields = ['file']
        labels = {'file': 'Plik'}


class UmowySearchForm(forms.Form):
    searched = forms.CharField(label='Search')