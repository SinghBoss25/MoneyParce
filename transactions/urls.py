from django.urls import path
from .views import dashboard_view, add_transaction

app_name = 'transactions'

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('add/', add_transaction, name='add_transaction'),
]
