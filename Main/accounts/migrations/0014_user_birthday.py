# Generated by Django 5.0.2 on 2024-02-19 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_remove_user_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.CharField(blank=True, null=True),
        ),
    ]
