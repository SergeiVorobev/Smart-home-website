from django import forms
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


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


class Location(models.Model):
    country = models.CharField('Country', max_length=50)
    city = models.CharField('City', max_length=50)
    street = models.CharField('Street', max_length=50)
    house = models.CharField('House', max_length=50)
    place = models.CharField('Place', max_length=50)
    postal = models.CharField('Postal/Zip', default='', max_length=50)
    users = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
    add_description = models.TextField('Description', blank=True)


class Device(models.Model):
    type = models.CharField('Type', max_length=50)
    description = models.TextField('Description', blank=True)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    isWorking = models.BooleanField(default=True)


class Lights(models.Model):
    place = models.CharField('Place', max_length=50)
    is_working = models.BooleanField(default=False)


# class Log(models.Model):
#     sensorOutput = models.CharField('Logs output', max_length=50)
#     time = models.TimeField()
#     transactionId = models.IntegerField()


