# Generated by Django 5.0.2 on 2024-04-22 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_rename_country_address_county'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='county',
        ),
    ]
