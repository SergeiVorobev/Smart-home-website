from django.urls import path
from . import views

urlpatterns =[
     path('', views.home, name="home"),
     path('register/', views.registration, name="registration"),
     path('login/', views.loginPage, name="login"),
     path('logout/', views.logoutUser, name="logout"),
     path('climate/', views.all_climate, name="climate"),
     path('lights/', views.all_lights, name="lights"),
     path('logs/', views.all_logs, name="logs"),

     path('settings/', views.settings, name="settings"),

]