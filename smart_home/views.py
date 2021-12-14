import smtplib

from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
# from .models import Device
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import Location, Profile

# from .models import UserAccount
from .forms import UpdateUserForm, UpdateProfileForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.views import generic
from django.views import View
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import RegisterForm, LoginForm, AddressForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

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


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/registration.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py

        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')

# class SuccessVisitView(SuccessMessageMixin, PasswordResetView):
#     template_name = 'users/login.html'
#     email_template_name = 'users/success_login.html'
#     subject_template_name = 'users/password_reset_subject'
#     success_message = "We inform you about visiting the Smart home system website with your login, " \
#                       # "if an account exists with the email you entered. You should receive them shortly." \
#                       # " If you don't receive an email, " \
#                       # "please make sure you've entered the address you registered with, and check your spam folder."
#     success_url = reverse_lazy('users-home')

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-profile')


@login_required(login_url='login')
def all_climate(request):
    # climate_list = Climate.objects.all().order_by('event_date')
    return render(request, 'climate.html')


@login_required(login_url='login')
def set_tings(request):
    address_list = Location.objects.all().order_by('street')
    user = Profile.objects.all().order_by('user_id')
    return render(request, 'settings.html',
                  {'address_list': address_list,
                   'person': user})


@login_required(login_url='login')
def all_lights(request):
    # climate_list = Climate.objects.all().order_by('event_date')
    return render(request, 'lights.html')


@login_required(login_url='login')
def all_logs(request):
    # climate_list = Climate.objects.all().order_by('event_date')
    return render(request, 'logs.html')


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required(login_url='login')
def edit_address(request, address_id):
    address = Location.objects.get(pk=address_id)
    form = AddressForm(request.POST or None, instance=address)
    if form.is_valid():
        form.save()
        return redirect('show-address', address_id)

    return render(request, 'edit_address.html', {'address': address, 'form': form})


# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.template.loader import render_to_string
#
# def success_login(request):
#
#     template = render_to_string('email_login.html', {'name': request.user.first_name})
#     # user = RegisterForm
#     mail = request.user.email
#     email = EmailMessage(
#         'You have been logged in',
#         # 'email_login.html',
#         template,
#         settings.EMAIL_HOST_USER,
#         [mail],
#     )
#     email.fail_silently=False
#     email.send()

    # messages.success(request, 'Your profile is updated successfully')
    # contex = {'user': user}
    #
    # return render(request, 'users/profile.html', contex)

# def send_message(to_email, body_message):
#
#     with smtplib.SMTP(settings.EMAIL_HOST, 587) as srv:
#         srv.ehlo()
#         srv.starttls()
#         srv.ehlo()
#         srv.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
#         now = datetime.now()
#         dt = now.strftime("%d/%m/%Y %H:%M:%S")
#         message = f'Subject: CoCo\n\n{dt} -- CoCo Administration\r\n\n{body_message}\n\nBest regards\nCoCo\'s team'
#         srv.sendmail(settings.EMAIL_HOST_USER, to_email, message)
#         srv.quit()

@login_required(login_url='login')
def add_address(request):
    submitted = False

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_address?submitted=True')
    else:
        form = AddressForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'add_address.html', {'form': form, 'submitted': submitted})


@login_required(login_url='login')
def show_address(request, address_id):
    address = Location.objects.get(pk=address_id)
    return render(request, 'show_address.html', {
                      "address": address,
                  })


def del_address(request, address_id):
    event = Location.objects.get(pk=address_id)
    event.delete()
    return redirect('settings')
