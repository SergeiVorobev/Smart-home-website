from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views
from .views import RegisterView, CustomLoginView, ResetPasswordView, profile, ChangePasswordView
from .forms import LoginForm

urlpatterns =[
     path('', views.home, name="users-home"),
     path('register/', RegisterView.as_view(), name="users-register"),
     path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=LoginForm), name='login'),
     path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
     url(r'^oauth/', include('social_django.urls', namespace='social')),
     path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
     path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

     path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('profile/', profile, name='users-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

                 # path('login/', views.loginPage, name="login"),
     # path('logout/', views.logoutUser, name="logout"),
     path('climate/', views.all_climate, name="climate"),
     path('lights/', views.all_lights, name="lights"),
     path('logs/', views.all_logs, name="logs"),
     # path('settings/', views.set_tings, name="settings"),
     # path('personal/', views.personal, name="person"),
     # path('edit_user/', views.edit_user, name="edit_profile"),
     path('edit_address/', views.edit_address, name="edit_address"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)