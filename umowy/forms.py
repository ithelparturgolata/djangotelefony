from django import forms
from django.utils.safestring import mark_safe

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
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.lower().endswith('.pdf'):
                error_message = mark_safe("<b><span style='color:red;'>Umowa format tylko pdf.</span></b>")
                raise forms.ValidationError(error_message)
        return file
    
    
class ContractFileFormAnnex(forms.ModelForm):
    class Meta:
        model = ContractFileAnnex
        fields = ['file_annex']
        labels = {'file_annex': 'Plik'}

    def clean_file_annex(self):
        file_annex = self.cleaned_data.get('file_annex')
        if file_annex:
            if not file_annex.name.lower().endswith('.pdf'):
                error_message = mark_safe("<b><span style='color:red;'>Aneks format tylko pdf.</span></b>")
                raise forms.ValidationError(error_message)
        return file_annex
    
    
class ContractsSearchForm(forms.Form):
    searched = forms.CharField(label='Search')