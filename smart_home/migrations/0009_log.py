# Generated by Django 3.2.8 on 2022-12-07 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_home', '0008_remove_location_place'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensorOutput', models.CharField(max_length=50, verbose_name='Logs output')),
                ('time', models.TimeField()),
                ('transactionId', models.IntegerField()),
            ],
        ),
    ]
