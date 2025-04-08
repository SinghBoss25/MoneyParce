from django import forms
from .models import BankConnection

class BankConnectionForm(forms.ModelForm):
    class Meta:
        model = BankConnection
        fields = ['bank_name', 'access_token']
