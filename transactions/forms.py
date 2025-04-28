from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type','amount', 'category', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['type'].widget = forms.RadioSelect(choices=Transaction.TRANSACTION_TYPES)

        self.fields['category'].queryset = Category.objects.none()

        self.fields['amount'].widget.attrs.update({
            'placeholder': 'Enter amount',
            'onfocus': "if(this.value=='0.00')this.value='';"
        })

        if 'type' in self.data:
            selected_type = self.data.get('type')
            self.fields['category'].queryset = Category.objects.filter(type=selected_type)
        elif self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)


