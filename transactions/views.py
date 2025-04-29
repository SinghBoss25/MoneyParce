from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from .models import Transaction, Category
from django.db import models
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
from openai import OpenAI
from django.conf import settings
from django.utils.html import format_html
from decimal import Decimal



def transactions_list(request):
    transactions = Transaction.objects.filter(user=request.user)

    total_income = sum(Decimal(t.amount) for t in transactions if t.type == 'income') or 0
    total_expenses = sum(Decimal(t.amount) for t in transactions if t.type == 'expense') or 0
    net_total = total_income - total_expenses

    return render(request, 'transactions/list.html', {
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_total': net_total,
    })

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

@login_required
def chat_view(request):
    conversation = request.session.get("chat_messages", [])

    if not conversation:
        greeting = "Hi! I'm your MoneyParce AI assistant. Ask me anything about your finances!"
        conversation.append({"role": "ai", "content": format_html(greeting)})

    request.session["chat_messages"] = conversation

    return render(request, "transactions/chat.html", {
        "messages": conversation
    })

openai_client = OpenAI(
    api_key=settings.TOGETHER_API_KEY,
    base_url="https://api.together.xyz/v1"
)

@csrf_exempt
@login_required
def chat_api(request):
    data = json.loads(request.body)
    user_message = data.get("message", "")

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:50]
    summary = "\n".join([f"{t.date}: {t.type} of ${t.amount} for {t.category.name}" for t in transactions])

    prompt = f"""
You are a helpful personal finance assistant. Here's the user's recent spending:

{summary}

They asked: {user_message}

Give helpful advice based on their spending.
"""

    response = openai_client.chat.completions.create(
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": prompt}]
    )
    ai_answer = response.choices[0].message.content
    return JsonResponse({"answer": ai_answer})