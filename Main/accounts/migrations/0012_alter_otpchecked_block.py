# Generated by Django 5.0.2 on 2024-02-11 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_otpchecked_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpchecked',
            name='block',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
