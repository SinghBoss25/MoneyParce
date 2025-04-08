from django.urls import path
from .views import set_budget

app_name = 'budgets'

urlpatterns = [
    path('set/', set_budget, name='set_budget'),
]
