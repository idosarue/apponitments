# Generated by Django 3.2.7 on 2021-09-05 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_appointmentresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentresponse',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
