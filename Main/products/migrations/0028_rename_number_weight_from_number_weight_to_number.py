# Generated by Django 5.0.2 on 2024-02-26 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_weight_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weight',
            old_name='number',
            new_name='from_number',
        ),
        migrations.AddField(
            model_name='weight',
            name='to_number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
