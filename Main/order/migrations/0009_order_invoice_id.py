# Generated by Django 5.0.2 on 2024-02-27 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_order_buy'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='invoice_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
