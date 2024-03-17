from django import forms
from .models import Contract, ContractFile, Contractor, ContractFileAnnex


class ContractForm(forms.ModelForm):
    # Override the end_date field to handle 'infinite' value
    end_date = forms.DateField(required=False, label='Czas nieokreślony')

    class Meta:
        model = Contract
        fields = ['contractor', 'description', 'start_date', 'end_date', 'place']
        labels = {'contractor': 'Wykonawca', 'files': 'Pliki', 'description': 'Opis', 'start_date': 'Umowa od', 'end_date': 'Umowa do', 'place': 'Umowa jest w:'}
    
    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date == "nieokreślony":
            return end_date  # Return "nieokreślony" if it's set
        return end_date  # Return the cleaned end_date value

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
        

class ContractFileFormAnnex(forms.ModelForm):
    class Meta:
        model = ContractFileAnnex
        fields = ['file_annex']
        labels = {'file_annex': 'Plik'}


class ContractsSearchForm(forms.Form):
    searched = forms.CharField(label='Search')