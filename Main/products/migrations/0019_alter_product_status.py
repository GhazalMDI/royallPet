# Generated by Django 5.0.2 on 2024-02-24 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_product_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('None', 'none'), ('color', 'Color'), ('Size', 'size'), ('colorSize', 'ColorSize'), ('Weight', 'weight')], default='None', max_length=20),
        ),
    ]
