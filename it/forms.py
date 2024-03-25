from django import forms
from .models import UsersIT


class UsersITForm(forms.ModelForm):
    class Meta:
        model = UsersIT
        fields = ['name', 'surname', 'administration', 'address_ip_pc', 'login', 'domain_name', 'office_pass', 'address_ip_phone', 'address_ip_phone_second', 'phone_pass']
        labels = {'name': 'Imię', 'surname': 'Nazwisko', 'administration': 'Administracja', 'address_ip_pc': 'Adres IP PC', 'login': 'Login', 'domain_name': 'PC Domena', 'office_pass': 'Hasło office', 'address_ip_phone': 'Adres IP Telefon', 'address_ip_phone_second': 'Drugi IP Telefon', 'phone_pass': 'Hasło Telefon'}
