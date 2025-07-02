from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Renders the main home page and the about page. Also includes a view
# that redirects the user to their transaction list if they are logged in,
# or to the signup page if they are a new visitor.def index(request):
    return render(request, 'home/index.html')
def about(request):
    return render(request, 'about.html')
def get_started_redirect(request):
    if request.user.is_authenticated:
        return redirect('transactions:list')
    else:
        return redirect('accounts.signup')
    