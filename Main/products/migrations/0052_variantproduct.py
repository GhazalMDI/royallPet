# Generated by Django 5.0.2 on 2024-04-06 12:44

import django.db.models.deletion
import django_jalali.db.models
import products.DiscountValidators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0051_brand_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariantProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('updated', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('price', models.PositiveIntegerField(default=0, validators=[products.DiscountValidators.PriceError])),
                ('discount', models.PositiveIntegerField(default=0, validators=[products.DiscountValidators.MaxDiscount])),
                ('stock', models.PositiveIntegerField(default=0, validators=[products.DiscountValidators.StockError])),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='var_color', to='products.color')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='var_product', to='products.product')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='var_size', to='products.size')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
