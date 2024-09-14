from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
    form = UserCreationForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"] 

            if User.objects.filter(username=username).exists():  # Corrected line
                messages.error(request, "This user already exists")
                return redirect("register")
            
            user = form.save()
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
    
    return render(request, "authenticate/registration.html", {'form': form})
