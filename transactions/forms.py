from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type','amount', 'category']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['type'].widget = forms.RadioSelect(choices=Transaction.TRANSACTION_TYPES)

        # Dynamically filter categories based on selected type
        self.fields['category'].queryset = Category.objects.none()

        if 'type' in self.data:
            selected_type = self.data.get('type')
            self.fields['category'].queryset = Category.objects.filter(type=selected_type)
        elif self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)


