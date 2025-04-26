from django.shortcuts import render, redirect
from .forms import BudgetForm, FinancialGoalForm
from .models import Budget, FinancialGoal
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from datetime import date
from django.shortcuts import render
from transactions.models import Transaction
from datetime import datetime
from collections import defaultdict

@login_required
def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'finance/set_budget.html', {'form': form})

@login_required
def edit_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'finance/set_budget.html', {'form': form})

@login_required
def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'finance/delete_confirm.html', {'object': budget, 'type': 'Budget'})

@login_required
def set_goal(request):
    if request.method == 'POST':
        form = FinancialGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goal_list')
    else:
        form = FinancialGoalForm()
    return render(request, 'finance/set_goal.html', {'form': form})

@login_required
def edit_goal(request, goal_id):
    goal = get_object_or_404(FinancialGoal, id=goal_id, user=request.user)
    if request.method == 'POST':
        form = FinancialGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goal_list')
    else:
        form = FinancialGoalForm(instance=goal)
    return render(request, 'finance/set_goal.html', {'form': form})

@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(FinancialGoal, id=goal_id, user=request.user)
    if request.method == 'POST':
        goal.delete()
        return redirect('goal_list')
    return render(request, 'finance/delete_confirm.html', {'object': goal, 'type': 'Goal'})

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'finance/budget_list.html', {'budgets': budgets})

@login_required
def goal_list(request):
    goals = FinancialGoal.objects.filter(user=request.user)
    return render(request, 'finance/goal_list.html', {'goals': goals})

@login_required
def dashboard(request):
    budgets = Budget.objects.filter(user=request.user)
    goals = FinancialGoal.objects.filter(user=request.user)

    total_budget = budgets.aggregate(Sum('amount'))['amount__sum'] or 0
    total_goals = goals.count()
    total_goal_progress = sum([g.progress() for g in goals]) / total_goals if total_goals else 0

    context = {
        'total_budget': total_budget,
        'total_goals': total_goals,
        'average_goal_progress': round(total_goal_progress, 2),
    }
    return render(request, 'finance/dashboard.html', context)




def monthly_summary(request):
    user = request.user
    month = request.GET.get('month')
    year = request.GET.get('year')

    if not month or not year:
        now = datetime.now()
        month = now.month
        year = now.year

    transactions = Transaction.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    )

    income_total = 0
    expense_total = 0
    category_totals = defaultdict(float)

    for t in transactions:
        if "income" in t.type.lower():
            income_total += float(t.amount)
        elif "expense" in t.type.lower():
            expense_total += float(t.amount)
            category_totals[str(t.category)] += float(t.amount)

    net_savings = income_total - expense_total
    if not category_totals:
        category_totals = {"No Data": 1}


    context = {
        'income': float(income_total),
        'expenses': float(expense_total),
        'net_savings': float(net_savings),
        'category_totals': dict(category_totals),
        'selected_month': month,
        'selected_year': year,
    }


    return render(request, 'finance/monthly_summary.html', context)
