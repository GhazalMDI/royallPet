# Generated by Django 5.0.2 on 2024-05-01 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0071_rename_unit_price_variantproduct_price'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SeenProduct',
        ),
    ]
