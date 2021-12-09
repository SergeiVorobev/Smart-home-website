from django import forms
from django.db import models
import uuid
from django.contrib.auth.models import User
from PIL import Image
import datetime
from datetime import date
from django.utils import timezone
from django.core.exceptions import ValidationError
# class MyUUIDModel(models.Model):
#     id = models.UUIDField(
#          primary_key = True,
#          default = uuid.uuid4,
#          editable = False)

# Extending User Model Using a One-To-One Link

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            rgb_im = img.convert('RGB')
            rgb_im.save(self.avatar.path)

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


# class UserAccount(models.Model):
#     username = models.CharField('User Name', max_length=50)
#     f_name = models.CharField('First Name', max_length=50)
#     l_name = models.CharField('Last Name', max_length=50)
#     email = models.EmailField('Email', blank=True)
#     phone = models.CharField('Phone Number', max_length=15, blank=True)
#
#     # type = models.CharField('Type of Venue', max_length=255)
#     def __str__(self):
#         return self.f_name

class Location(models.Model):
    country = models.CharField('Country', max_length=50)
    city = models.CharField('City', max_length=50)
    street = models.CharField('Street', max_length=50)
    house = models.CharField('House', max_length=50)
    place = models.CharField('Place', max_length=50)


class Device(models.Model):
    type = models.CharField('Type', max_length=50)
    description = models.TextField('Description', blank=True)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    isWorking = models.BooleanField(default=True)


class Lights(models.Model):
    place = models.CharField('Place', max_length=50)
    is_working = models.BooleanField(default=False)

#
# class Command(models.Model):
#     type = models.CharField('Type', max_length=50)
#     time = models.TimeField()
#     device = models.ForeignKey(Device, on_delete=models)
#
# class Profile(models.Model):
#     user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
#     isAway = models.BooleanField(default=False)
#     devices = models.ManyToManyField(Device, blank=True)
#
# class Action(models.Model):
#     isPossible = models.IntegerField()
#     channel = models.CharField('Channel', max_length=50)
#
# class Log(models.Model):
#     sensorOutput = models.CharField('Logs output', max_length=50)
#     time = models.TimeField()
#     transactionId = models.IntegerField()


