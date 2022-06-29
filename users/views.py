from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer


# Create your views here.
def register_user(request):
    # shouldnt be able to register is already logged in
    if request.user.is_authenticated:
        return redirect('profile')

    # check if post request
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        # validate
        if form.is_valid():
            # take creds
            user = form.save()
            username = form.cleaned_data.get('username')

            # create and save new customer
            new_customer = Customer(
                user=user, username=user.username, email=user.email,
                fname=user.first_name, lname=user.last_name
            )
            new_customer.save()

            messages.success(request, f'Your account has been created. Please log in to continue. {username}!')
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def login_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('search')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'users/login.html', context)


@login_required
def profile(request):
    return render(request, 'users/profile.html')