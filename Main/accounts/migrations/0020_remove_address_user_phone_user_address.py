# Generated by Django 5.0.2 on 2024-04-08 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user_phone',
        ),
        migrations.AddField(
            model_name='user',
            name='Address',
            field=models.ManyToManyField(related_name='user_address', to='accounts.address'),
        ),
    ]
