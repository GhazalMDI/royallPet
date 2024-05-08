# Generated by Django 5.0.2 on 2024-04-09 09:41

import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0065_remove_comment_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('updated', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_like', to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_like', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
