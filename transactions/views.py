from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transactions/dashboard.html', {'transactions': transactions})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            trans = form.save(commit=False)
            trans.user = request.user
            trans.save()
            return redirect('transactions:dashboard')
    else:
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html', {'form': form})
