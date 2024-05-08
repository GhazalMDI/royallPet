# Generated by Django 5.0.2 on 2024-02-23 16:23

import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_categorysub_product_category3'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('updated', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('name', models.CharField(choices=[('None', 'هیچکدام'), ('red', 'قرمز'), ('blue', 'آبی'), ('green', 'سبز'), ('yellow', 'زرد'), ('black', 'مشکی'), ('orange', 'نارنجی'), ('white', 'سفید')], default='None', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('updated', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('Unit', models.CharField(choices=[('gram', 'g'), ('kilogram', 'kg')], default='gram', max_length=40)),
                ('number', models.CharField(choices=[('fifty', '50'), ('seventyfive', '75'), ('Hundred', '100'), ('onehandredfifty', '150'), ('twoHundred', '200'), ('threeHundred', '300'), ('fourHundred', '400'), ('fiveHundred', '500'), ('sixHundred', '600'), ('sevenHundred', '700'), ('Thousand', '1'), ('twoThousand', '2'), ('threeThousand', '3')], default='fifty', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
