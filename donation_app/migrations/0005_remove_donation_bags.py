# Generated by Django 4.2.6 on 2024-04-07 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donation_app', '0004_donation_bags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation',
            name='bags',
        ),
    ]
