# Generated by Django 4.2.6 on 2023-10-27 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coolapp', '0002_district_coolapp_dis_name_f7e06d_idx'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='district',
            options={'verbose_name': 'District', 'verbose_name_plural': 'Districts'},
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
                'indexes': [models.Index(fields=['district', 'average_temperature_2pm'], name='coolapp_tem_distric_e2aa47_idx')],
            },
        ),
    ]