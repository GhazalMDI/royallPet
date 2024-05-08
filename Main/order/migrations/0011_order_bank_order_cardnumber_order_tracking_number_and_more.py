# Generated by Django 5.0.2 on 2024-02-27 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_order_err_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bank',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='cardnumber',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='tracking_number',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='transid',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
