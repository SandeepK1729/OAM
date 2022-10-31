from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import login as auth_login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    
    return render(request, 'home.html', {
        'count' : User.objects.count(),
    })

def signup(request):
    if request.method == 'POST':    
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {
        'form' : form,
    })

def about(request):
    return render(request, 'about.html')