from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from telefony.models import Mieszkaniec, Blok
from django import forms
from django.forms.widgets import PasswordInput, TextInput, FileInput


# class SmsRecordFormSms(forms.ModelForm):
#     class Meta:
#         model = Mieszkaniec
#         content = forms.CharField(widget=forms.Textarea,
#                                   label="tekst", max_length=160)
#         phone = forms.CharField(widget=forms.Textarea,
#                                 label="Telefon", max_length=10000)
#         fields = ["phone", "content"]

class SmsRecordFormSms(forms.ModelForm):
    class Meta:
        model = Mieszkaniec
        fields = ["indeks", "nazwa", "phone", "content", "telefon"]

class SmsRecordFormSmsBlok(forms.ModelForm):
    class Meta:
        model = Mieszkaniec
        fields = ["phone", "content"]
