# Generated by Django 4.2.6 on 2023-10-28 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coolapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='temperatureforecast',
            name='travel_date',
            field=models.DateTimeField(null=True),
        ),
    ]