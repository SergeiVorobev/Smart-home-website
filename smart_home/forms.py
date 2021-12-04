from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# class ChangeUser(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']