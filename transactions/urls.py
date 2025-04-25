from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.transactions_list, name='list'),
    path('add/', views.add_transaction, name='add'),
    path('edit/<int:transaction_id>/', views.add_transaction, name='edit'),
    path('delete/<int:transaction_id>/', views.delete_transaction, name='delete'),
    path('plaid/create-link-token/', views.create_link_token, name='create_link_token'),
    path('plaid/exchange-token/', views.exchange_public_token, name='exchange_token'),
    path('import/', views.import_transactions, name='import_transactions'),
    path("chat/", views.chat_view, name="chat"),
    path("chat-api/", views.chat_api, name="chat_api"),
]
