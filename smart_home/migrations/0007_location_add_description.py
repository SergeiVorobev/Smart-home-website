# Generated by Django 3.2.8 on 2021-12-13 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_home', '0006_auto_20211213_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='add_description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
    ]
