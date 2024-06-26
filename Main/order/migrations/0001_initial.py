# Generated by Django 5.0.2 on 2024-02-24 14:02

import django.db.models.deletion
import django_jalali.db.models
import products.DiscountValidators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0019_alter_product_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('updated', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('f_name', models.CharField(blank=True, max_length=255, null=True)),
                ('l_name', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField()),
                ('postal_code', models.CharField(max_length=10)),
                ('paid', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_order', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('updated', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('price', models.PositiveIntegerField(default=0, validators=[products.DiscountValidators.PriceError])),
                ('quantity', models.PositiveIntegerField(default=0, validators=[products.DiscountValidators.StockError])),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_item', to='order.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_order_item', to='products.product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
