from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def login_view(request):
    # This will use Django's built-in auth views or a custom one later
    # For now, we'll just render a placeholder if needed, but usually 
    # we configure this in urls.py directly to use auth_views.LoginView
    pass