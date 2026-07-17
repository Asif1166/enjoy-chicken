from django.conf import settings
from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
User  = settings.AUTH_USER_MODEL
# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, Your account was created successfully")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'authentication/reg.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request, f"User with {email} does not exist")
            
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"You are loged in.")
            return redirect('home')
        
        else:
            messages.warning(request, "User does not exist, create an account")
            
    context = {
        
    }
    
    return render(request, "authentication/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")