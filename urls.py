from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('transactions.urls')),
    path('budgets/', include('budgets.urls')),
    path('banks/', include('bank_sync.urls')),
    path('reports/', include('reports.urls')),
    #path('ai/', include('ai_advice.urls')),
]
