# Generated by Django 4.0.5 on 2022-06-19 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trader',
            name='notifications_status',
            field=models.BooleanField(default=False),
        ),
    ]
