from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from .models import Transaction
from django.http import JsonResponse
from .plaid_client import client
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from plaid2.model.link_token_create_request_user import LinkTokenCreateRequestUser

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

@login_required
def create_link_token(request):
    user_model = LinkTokenCreateRequestUser(client_user_id=str(request.user.id))
    response = client.link_token_create(
        user=user_model,
        client_name="MoneyParce",
        products=["transactions"],
        country_codes=["US"],
        language="en"
    )
    return JsonResponse(response.dict(), safe=False)

@csrf_exempt
@login_required
def exchange_public_token(request):
    data = json.loads(request.body)
    public_token = data.get('public_token')
    exchange = client.item_public_token_exchange(public_token)
    access_token = exchange['access_token']
    
    # Save this token to your user or profile model
    request.user.profile.plaid_access_token = access_token
    request.user.profile.save()

    return JsonResponse({'status': 'success'})
