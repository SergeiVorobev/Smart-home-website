from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
# from .models import Device
from django.urls import reverse_lazy
from .models import UserAccount
from .forms import CreateUser
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.
@login_required(login_url='login')
def home(request):

    # Get current year
    now = datetime.now()
    year_ = now.strftime('%Y')
    date_ = now.strftime("%d %B %Y, ")
    hours = now.strftime('%H')
    hours = int(hours) + 1
    hours = str(hours)
    time_ = hours + now.strftime(':%M:%S')
    return render(request, 'home.html', {
       'date': date_,
        'year': year_,
        'time' : time_,
    })


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

        if request.method == 'POST':
            form = CreateUser(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'registration.html', context)

@login_required(login_url='login')
def edit_user(request):

    form = CreateUser()

    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was updated for ' + user)
            return redirect('settings')

    context = {'form': form}
    return render(request, 'edit_profile.html', context)

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

def loginPage(request):

    if request.user.is_authenticated:
        from_mail = settings.EMAIL_HOST_USER
        user = UserAccount.objects.all()
        name = user.f_name
        e_mail = user.email
        print(e_mail)
        template = render_to_string('email_template.html', {'name': name})
        send_mail(
                'You logged into CoCo',
                template,
                from_mail,
                [e_mail],
        )

        # email = EmailMessage(
        #     'You logged into CoCo',
        #     template,
        #     from_mail,
        #     [e_mail],
        #
        # )
        # email.send(fail_silently=False)

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
def set_tings(request):
    # climate_list = Climate.objects.all().order_by('event_date')
    form = CreateUser(request.GET)

    user = request.user
    last_name = request.POST.get('last_name')
    email = form.data.get('email')

    return render(request, 'settings.html',
                  {"username": user,
                    "l_name": last_name,
                    "e_mail": email,
                    })

@login_required(login_url='login')
def personal(request):
    # climate_list = Climate.objects.all()
    return render(request, 'personal.html')


@login_required(login_url='login')
def edit_address(request):
    return render(request, 'edit_address.html')
