# Generated by Django 4.2.16 on 2024-09-28 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_workingday_doctor_description_doctor_working_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]