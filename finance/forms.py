from django import forms
from .models import Budget, FinancialGoal

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month']

class FinancialGoalForm(forms.ModelForm):
    class Meta:
        model = FinancialGoal
        fields = ['name', 'target_amount', 'current_amount', 'deadline']
