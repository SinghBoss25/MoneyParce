from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
def transactions_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.user = request.user
            new_transaction.save()
            return redirect('transactions')
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transactions.html', {'form': form, 'transactions': transactions})
