from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BankConnectionForm
from .models import BankConnection

@login_required
def connect_bank(request):
    if request.method == 'POST':
        form = BankConnectionForm(request.POST)
        if form.is_valid():
            connection = form.save(commit=False)
            connection.user = request.user
            connection.save()
            return redirect('transactions:dashboard')
    else:
        form = BankConnectionForm()
    return render(request, 'bank_sync/connect_bank.html', {'form': form})
