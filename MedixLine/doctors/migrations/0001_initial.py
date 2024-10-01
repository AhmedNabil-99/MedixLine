<<<<<<< HEAD
# Generated by Django 4.2.16 on 2024-09-30 14:29
=======
# Generated by Django 4.2.16 on 2024-09-30 21:53
>>>>>>> cb85a61eca45bf43440521954993eb3cdd762b0e

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('image', models.ImageField(upload_to='specialization/images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
            ],
        ),
        migrations.CreateModel(
            name='WorkingDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('address', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message='Not A Valid Phone Number.', regex='^(010|011|015|012)\\d{8}$')])),
                ('profile_picture', models.ImageField(upload_to='doctors/images/profile_pic', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
                ('national_id', models.ImageField(upload_to='doctors/images/national_ids', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
                ('syndicate_id', models.ImageField(upload_to='doctors/images/syndicate_ids', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
                ('is_confirmed', models.BooleanField(default=False)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('specialization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='doctors.specialization')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_account', to=settings.AUTH_USER_MODEL)),
                ('working_days', models.ManyToManyField(blank=True, null=True, related_name='doctor_working_days', to='doctors.workingday')),
            ],
        ),
    ]
