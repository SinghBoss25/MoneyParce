from django.shortcuts import render, redirect
from .forms import TransactionForm
from .models import Transaction

def transactions_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transactions/list.html', {'transactions': transactions})

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transactions:list')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'transactions/add.html', {'form': form})
