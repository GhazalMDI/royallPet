# Generated by Django 5.0.2 on 2024-02-24 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_alter_weight_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weight',
            name='number',
            field=models.CharField(choices=[('None', 'هیچکدام'), ('50', '50'), ('75', '75'), ('95', '95'), ('85', '85'), ('100', '100'), ('120', '120'), ('150', '150'), ('200', '200'), ('300', '300'), ('400', '400'), ('500', '500'), ('600', '600'), ('700', '700'), ('1', '1'), ('2', '2'), ('3', '3')], default='fifty', max_length=20),
        ),
    ]
