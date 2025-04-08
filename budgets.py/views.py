from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Budget
from .forms import BudgetForm

@login_required
def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('transactions:dashboard')
    else:
        form = BudgetForm()
    return render(request, 'budgets/set_budget.html', {'form': form})
