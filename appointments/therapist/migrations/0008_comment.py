# Generated by Django 3.2.7 on 2021-09-20 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('therapist', '0007_auto_20210919_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=255)),
            ],
        ),
    ]
