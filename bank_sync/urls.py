from django.urls import path
from .views import connect_bank

app_name = 'bank_sync'

urlpatterns = [
    path('connect/', connect_bank, name='connect_bank'),
]
