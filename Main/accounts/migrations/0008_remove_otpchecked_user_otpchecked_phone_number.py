# Generated by Django 5.0.2 on 2024-02-10 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_otpchecked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otpchecked',
            name='user',
        ),
        migrations.AddField(
            model_name='otpchecked',
            name='phone_number',
            field=models.CharField(max_length=11, null=True),
        ),
    ]