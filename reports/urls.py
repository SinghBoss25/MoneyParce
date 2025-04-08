from django.urls import path
from .views import monthly_summary

app_name = 'reports'

urlpatterns = [
    path('summary/', monthly_summary, name='summary'),
]
