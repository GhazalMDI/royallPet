# Generated by Django 5.0.2 on 2024-02-24 06:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_size_variantproduct_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variantproduct',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='var_color', to='products.color'),
        ),
        migrations.AlterField(
            model_name='variantproduct',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='var_size', to='products.size'),
        ),
        migrations.AlterField(
            model_name='variantproduct',
            name='weight',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='var_weight', to='products.weight'),
        ),
    ]