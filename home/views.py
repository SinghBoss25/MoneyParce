from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'home/index.html')
def about(request):
    return render(request, 'about.html')
def get_started_redirect(request):
    if request.user.is_authenticated:
        return redirect('transactions:list')
    else:
        return redirect('accounts.signup')
    