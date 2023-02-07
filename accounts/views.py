from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import ListView

from accounts.forms import CreateUserAccount
from room_booking_app.models import User


# Create your views here.
def register(request):
    if request.method == "POST":
        form = CreateUserAccount(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'account created successfully')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)

            return redirect('dashboard')
    else:
        form = CreateUserAccount()
    templatename = 'accounts/register.html'
    context = {'form': form}
    return render(request, templatename, context)


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = messages.error(request, 'Invalid details try again!!')
            templatename = 'accounts/signin.html'
            context = {"error": error}
            return render(request, templatename, context)
    else:
        templatename = 'accounts/signin.html'
        return render(request, templatename)


def signout(request):
    logout(request)
    return redirect('signin')


# -------------------Admin--page---------------------

def adminstrator(request):
    templatename = 'accounts/adminstrator_panel.html'
    context = {}
    return render(request, templatename, context)


class UsersListView(ListView):
    model = User
    context_object_name = 'users'
    ordering = 'updated_at'
    template_name = 'adminstrator/users.html'
