# Generated by Django 5.0.2 on 2024-02-26 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_remove_weight_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='weight',
            name='number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]