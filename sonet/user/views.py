from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import SignUpForm


# Create your views here.

def log_in(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('feed:index')
        
        else:
            messages.error(request, "Incorrect username or password")
            return redirect('login')

    else:
        return render(request, "authenticate/login.html", {})
    

def log_out(request):
    logout(request)
    return redirect('login')



def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            

            # Authenticate and log the user in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('feed:index')
            else:
                messages.error(request, "Failed to authenticate user after registration")
                return redirect('login')
        else:
            messages.error(request, "Form is not valid")
            return redirect('register')
    else:
        form = SignUpForm()

    return render(request, "authenticate/registration.html", {'form': form})
