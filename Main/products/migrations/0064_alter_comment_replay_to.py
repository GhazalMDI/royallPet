# Generated by Django 5.0.2 on 2024-04-07 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0063_comment_is_replay_comment_replay_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='replay_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replay_comment', to='products.comment'),
        ),
    ]