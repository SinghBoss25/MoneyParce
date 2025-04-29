from django import forms
from .models import Budget, FinancialGoal
from transactions.models import Transaction, Category

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.none()

        self.fields['amount'].widget.attrs.update({
            'placeholder': 'Enter amount',
            'onfocus': "if(this.value=='0.00')this.value='';"
        })
        self.fields['category'].queryset = Category.objects.filter(type='expense')

class FinancialGoalForm(forms.ModelForm):
    class Meta:
        model = FinancialGoal
        fields = ['name', 'target_amount', 'current_amount', 'deadline']
