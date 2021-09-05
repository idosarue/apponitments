# Generated by Django 3.2.7 on 2021-09-05 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_alter_appointment_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='choice',
            field=models.CharField(choices=[('A', 'ACCEPT'), ('P', 'PENDING')], max_length=10, null=True),
        ),
    ]
