# Generated by Django 5.0.2 on 2024-02-25 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
