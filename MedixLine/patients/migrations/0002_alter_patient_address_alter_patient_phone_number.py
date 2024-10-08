# Generated by Django 4.2.16 on 2024-10-05 12:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Not A Valid Phone Number.', regex='^(010|011|015|012)\\d{8}$')]),
        ),
    ]
