from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
# from .models import Device
from .forms import CreateUser
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


# @login_required(login_url='login')
# def all_devices(request):
#     devices_list = Device.objects.all().order_by('name')
#     return render(request, 'devices.html', {
#                       "device_list": devices_list,
#                      })

def registration(request):
    if request.user.is_authenticated:
        return redirect('base')
    else:
        form = CreateUser()

        if request.method=='POST':
            form = CreateUser(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'registration.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, password=password, username=username)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is not correct')

        context = {}
        return render(request, 'login.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def all_climate(request):
    # climate_list = Climate.objects.all().order_by('event_date')
    return render(request, 'climate.html')

@login_required(login_url='login')
def all_lights(request):
    # climate_list = Climate.objects.all().order_by('event_date')
    return render(request, 'lights.html')

@login_required(login_url='login')
def all_logs(request):
    # climate_list = Climate.objects.all().order_by('event_date')
    return render(request, 'logs.html')

@login_required(login_url='login')
def settings(request):
    # climate_list = Climate.objects.all().order_by('event_date')
    return render(request, 'settings.html')

@login_required(login_url='login')
def personal(request):
    # climate_list = Climate.objects.all().order_by('event_date')
    return render(request, 'personal.html')

@login_required(login_url='login')
def edit_profile(request):
    return render(request, 'edit_profile.html')

@login_required(login_url='login')
def edit_address(request):
    return render(request, 'edit_address.html')
