# Generated by Django 5.0.2 on 2024-03-26 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0038_remove_variantproduct_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(choices=[('None', 'none'), ('red', 'قرمز'), ('blue', 'آبی'), ('green', 'سبز'), ('yellow', 'زرد'), ('black', 'مشکی'), ('orange', 'نارنجی'), ('white', 'سفید')], default='None', max_length=20),
        ),
    ]
