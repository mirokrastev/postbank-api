# Generated by Django 4.0.5 on 2022-06-18 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panels', '0002_alter_discount_status_employeediscountaction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='is_locked',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
