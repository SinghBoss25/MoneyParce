from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from .models import Transaction, Category
from django.http import JsonResponse
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from datetime import date, timedelta
from django.views.decorators.csrf import csrf_exempt
from .plaid_client import client
import json

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
    user = LinkTokenCreateRequestUser(client_user_id=str(request.user.id))
    request_data = LinkTokenCreateRequest(
        user=user,
        client_name="MoneyParce",
        products=[Products("transactions")],
        country_codes=[CountryCode("US")],
        language="en"
    )
    response = client.link_token_create(request_data)
    return JsonResponse(response.to_dict())

@csrf_exempt
@login_required
def exchange_public_token(request):
    data = json.loads(request.body)
    exchange_request = ItemPublicTokenExchangeRequest(public_token=data["public_token"])
    exchange_response = client.item_public_token_exchange(exchange_request)
    
    access_token = exchange_response['access_token']
    request.user.profile.plaid_access_token = access_token
    request.user.profile.save()

    return JsonResponse({"status": "success"})

@login_required
def import_transactions(request):
    access_token = request.user.profile.plaid_access_token
    start_date = date.today() - timedelta(days=30)
    end_date = date.today()

    req = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date
    )
    response = client.transactions_get(req)
    plaid_transactions = response.to_dict()["transactions"]

    for tx in plaid_transactions:
        category_name = tx.get("category", ["Other"])[0]
        tx_type = "expense" if tx["amount"] > 0 else "income"
        category_obj, _ = Category.objects.get_or_create(name=category_name, defaults={"type": tx_type})

        if not Transaction.objects.filter(description=tx["transaction_id"]).exists():
            Transaction.objects.create(
                user=request.user,
                type=tx_type,
                amount=abs(tx["amount"]),
                category=category_obj,
                date=tx["date"],
                description=tx["name"] + f" ({tx['transaction_id']})"
            )

    return redirect("transactions:list")