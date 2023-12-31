# Generated by Django 4.2.6 on 2023-10-28 04:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('bn_name', models.CharField(max_length=100, verbose_name='Bangla Name')),
                ('lat', models.CharField(max_length=20, verbose_name='Latitude')),
                ('long', models.CharField(max_length=20, verbose_name='Longitude')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created At')),
                ('last_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Last Updated')),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
            },
        ),
        migrations.CreateModel(
            name='TemperatureForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('generationtime_ms', models.FloatField()),
                ('utc_offset_seconds', models.IntegerField()),
                ('timezone', models.CharField(max_length=255)),
                ('timezone_abbreviation', models.CharField(max_length=10)),
                ('elevation', models.FloatField()),
                ('hourly_units_time', models.CharField(max_length=255)),
                ('hourly_units_temperature_2m', models.CharField(max_length=10)),
                ('hourly_time', models.JSONField()),
                ('hourly_temperature_2m', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('last_updated', models.DateTimeField(verbose_name='Last Updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coolapp.district')),
            ],
        ),
        migrations.CreateModel(
            name='TemperatureData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_temperature_2pm', models.DecimalField(decimal_places=1, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('last_updated', models.DateTimeField(verbose_name='Last Updated')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coolapp.district')),
            ],
            options={
                'verbose_name': 'Temperature Data',
            },
        ),
        migrations.AddIndex(
            model_name='district',
            index=models.Index(fields=['name', 'bn_name', 'lat', 'long'], name='coolapp_dis_name_f7e06d_idx'),
        ),
        migrations.AddIndex(
            model_name='temperaturedata',
            index=models.Index(fields=['district', 'average_temperature_2pm'], name='coolapp_tem_distric_e2aa47_idx'),
        ),
    ]
