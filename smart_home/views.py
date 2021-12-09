from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
# from .models import Device
from django.urls import reverse_lazy
from django.views.generic import UpdateView

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
from .forms import RegisterForm, LoginForm
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


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

# def registration(request):
#     if request.user.is_authenticated:
#         return redirect('base')
#     else:
#         form = CreateUser()
#
#         if request.method == 'POST':
#             form = CreateUser(request.POST)
#             if form.is_valid():
#                 form.save()
#                 user = form.cleaned_data.get('username')
#                 messages.success(request, 'Account was created for ' + user)
#                 return redirect('login')
#
#         context = {'form': form}
#         return render(request, 'registration.html', context)



# @login_required(login_url='login')

# def edit_user(request):
#     if request.method == 'POST':
#         user_form = UpdateUserForm(request.POST, instance=request.user)
#         profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile is updated successfully')
#             return redirect(to='users-profile')
#     else:
#         user_form = UpdateUserForm(instance=request.user)
#         profile_form = UpdateProfileForm(instance=request.user.)
#
#     return render(request, 'users/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})



# def edit_user(request):
#
#     form = ChangeUser()
#     template = 'edit_profile.html'

    # form = ChangeUser()

    # if request.method == 'POST':
    #     form = ChangeUser(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         user = form.cleaned_data.get('username')
    #         messages.success(request, 'Account was updated for ' + user)
    #         return redirect('settings')
    #
    # context = {'form': form}
    # return render(request, 'edit_profile.html', context)

# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.template.loader import render_to_string
# from django.core.mail import send_mail
# import smtplib
#
# def loginPage(request):
#
#     if request.user.is_authenticated:
#         from_mail = settings.EMAIL_HOST_USER
#         user = UserAccount.objects.all()
#         name = user.f_name
#         e_mail = user.email
#         template = render_to_string('email_login.html', {'name': name})
#         print('Hello')
#         print(e_mail, template)
#
#         # send_message('vorobevse86@gmail.com', 'Hello')
#
#         # send_message(e_mail, template)
#         send_mail(
#                 'You logged into CoCo',
#                 template,
#                 from_mail,
#                 [e_mail],
#                  fail_silently=False,
#
#         )
#
#         # email = EmailMessage(
#         #     'You logged into CoCo',
#         #     template,
#         #     from_mail,
#         #     [e_mail],
#         #
#         # )
#         # email.send(fail_silently=False)
#
#         return redirect('home')
#     else:
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, password=password, username=username)
#
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 messages.info(request, 'Username or Password is not correct')
#
#         context = {}
#         return render(request, 'users/login.html', context)

# @login_required(login_url='login')
# def logoutUser(request):
#     logout(request)
#     return redirect('login')


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

# @login_required(login_url='login')
# def set_tings(request):
#     # climate_list = Climate.objects.all().order_by('event_date')
#     form = CreateUser(request.GET)
#
#     user = request.user
#     # last_name = UserAccount.objects.all()
#     # email = UserAccount.objects.all()
#
#     last_name = request.POST.get('last_name')
#     email = form.data.get('email')
#
#     return render(request, 'settings.html',
#                   {"username": user,
#                     "l_name": last_name,
#                     "e_mail": email,
#                     })

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
def edit_address(request):
    return render(request, 'edit_address.html')


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
