# Generated by Django 5.0.2 on 2024-05-01 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_alter_address_postal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='کد پستی'),
        ),
    ]
