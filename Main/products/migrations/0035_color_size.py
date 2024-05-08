# Generated by Django 5.0.2 on 2024-03-26 07:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0034_newproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='color_size', to='products.size'),
        ),
    ]
