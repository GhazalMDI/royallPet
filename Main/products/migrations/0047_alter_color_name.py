# Generated by Django 5.0.2 on 2024-03-29 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0046_alter_color_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(choices=[('None', 'none'), ('قرمز', 'قرمز'), ('آبی', 'آبی'), ('سبز', 'yellow'), ('yellow', 'red'), ('black', 'black'), ('orange', 'orange'), ('white', 'white')], default='None', max_length=20),
        ),
    ]