from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from .models import Transaction

@login_required
def transactions_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-id')
    return render(request, 'transactions/list.html', {'transactions': transactions})

@login_required
def add_transaction(request, transaction_id=None):
    if transaction_id:
        transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
        form = TransactionForm(request.POST or None, instance=transaction)
    else:
        transaction = None
        form = TransactionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        transaction = form.save(commit=False)
        if not transaction_id:
            # Only assign user on create, not on edit (already has a user)
            transaction.user = request.user
        transaction.save()
        return redirect('transactions:list')

    return render(request, 'transactions/add.html', {
        'form': form,
        'transaction': transaction
    })
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return redirect('transactions:list')
