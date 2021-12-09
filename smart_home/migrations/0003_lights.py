# Generated by Django 3.2.8 on 2021-12-08 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_home', '0002_device_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=50, verbose_name='Place')),
                ('is_working', models.BooleanField(default=False)),
            ],
        ),
    ]
