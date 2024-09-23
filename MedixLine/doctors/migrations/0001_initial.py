# Generated by Django 4.2.16 on 2024-09-23 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('profile_picture', models.ImageField(upload_to='doctors/images/profile_pic')),
                ('national_id', models.ImageField(upload_to='doctors/images/national_ids')),
                ('syndicate_id', models.ImageField(upload_to='doctors/images/syndicate_ids')),
                ('specialization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='doctors.specialization')),
            ],
        ),
    ]
