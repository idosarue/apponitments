# Generated by Django 3.2.7 on 2021-09-15 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_appointment_is_cancelled'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='date_t',
            field=models.DateTimeField(null=True),
        ),
    ]
