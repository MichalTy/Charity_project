# Generated by Django 4.2.6 on 2024-04-08 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_app', '0005_remove_donation_bags'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=False),
        ),
    ]
