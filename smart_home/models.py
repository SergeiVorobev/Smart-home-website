from django.db import models
import uuid
from django.contrib.auth.models import User
import datetime
from datetime import date
from django.utils import timezone
from django.core.exceptions import ValidationError

# class MyUUIDModel(models.Model):
#     id = models.UUIDField(
#          primary_key = True,
#          default = uuid.uuid4,
#          editable = False)

# class UserAccount(models.Model):
#     username = models.CharField('User Name', max_length=50)
#     f_name = models.CharField('First Name', max_length=50)
#     l_name = models.CharField('Last Name', max_length=50)
#     email = models.EmailField('Email', blank=True)
#     phone = models.CharField('Phone Number', max_length=15, blank=True)
#
# class Location(models.Model):
#     country = models.CharField('Country', max_length=50)
#     city = models.CharField('City', max_length=50)
#     street = models.CharField('Street', max_length=50)
#     house = models.CharField('House', max_length=50)
#     place = models.CharField('Place', max_length=50)
#
#
# class Device(models.Model):
#     type = models.CharField('Type', max_length=50)
#     description = models.TextField('Description', blank=True)
#     location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
#     isWorking = models.BooleanField(default=True)
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


