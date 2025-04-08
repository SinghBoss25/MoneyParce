from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction
from django.db.models import Sum
from collections import defaultdict

@login_required
def monthly_summary(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)
    
    category_totals = defaultdict(float)
    for txn in transactions:
        category_totals[txn.category] += txn.amount

    return render(request, 'reports/summary.html', {
        'category_totals': dict(category_totals),
        'transactions': transactions
    })
