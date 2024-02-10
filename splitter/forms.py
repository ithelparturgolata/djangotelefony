from django import forms

class PDFSplitForm(forms.Form):
    pdf_file = forms.FileField(label='Select a PDF file')
    destination_folder = forms.CharField(label='Destination folder', max_length=100)
    file_name = forms.CharField(label='File name', max_length=100)