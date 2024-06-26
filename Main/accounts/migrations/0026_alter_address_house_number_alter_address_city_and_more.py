# Generated by Django 5.0.2 on 2024-04-22 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_address_county'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='House_number',
            field=models.CharField(max_length=255, null=True, verbose_name='پلاک'),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=255, null=True, verbose_name='شهر'),
        ),
        migrations.AlterField(
            model_name='address',
            name='county',
            field=models.CharField(max_length=255, null=True, verbose_name='شهرستان'),
        ),
        migrations.AlterField(
            model_name='address',
            name='floor',
            field=models.CharField(max_length=255, null=True, verbose_name='طبقه'),
        ),
        migrations.AlterField(
            model_name='address',
            name='formatted_address',
            field=models.TextField(verbose_name='نشانی پستی'),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(max_length=255, verbose_name='استان'),
        ),
        migrations.AlterField(
            model_name='address',
            name='unit',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='واحد'),
        ),
        migrations.AlterField(
            model_name='address',
            name='village',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='روستا'),
        ),
    ]
