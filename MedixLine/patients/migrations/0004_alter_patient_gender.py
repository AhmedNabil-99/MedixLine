# Generated by Django 4.2.16 on 2024-10-06 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_alter_patient_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(max_length=10),
        ),
    ]
