# Generated by Django 5.0.2 on 2024-02-10 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seen_user',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
