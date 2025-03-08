from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import CustomUser

# Register a new user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful!")
            return redirect('visitors:identify')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('visitors:identify')  # or wherever you want to redirect
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'user/login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('user:login')
