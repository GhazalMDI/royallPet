# Generated by Django 5.0.2 on 2024-02-16 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_remove_product_seen_user_seenproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_sub',
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
    ]
