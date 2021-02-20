from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from users.forms import CustomUserCreationForm


# Create your views here.

def dashboard(request):
    print("users / views / dashboard")
    return render(request, "users/dashboard.html")


def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)        
        if form.is_valid():            
            user = form.save()            
            login(request, user)
            return redirect(reverse("dashboard"))
        else:            
            return render(
                request, "users/register.html",
                {
                    "form": CustomUserCreationForm,
                    "error_message": "The same user probably already exists."
                }
            )


def show(request):
    import os
    print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    if request.user.is_authenticated:
        return HttpResponse("you are logged in")
    else:
        return HttpResponse("You are NOT logged in.")