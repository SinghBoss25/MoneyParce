from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.transactions_list, name='list'),
    path('add/', views.add_transaction, name='add'),
    path('edit/<int:transaction_id>/', views.add_transaction, name='edit'),
]
