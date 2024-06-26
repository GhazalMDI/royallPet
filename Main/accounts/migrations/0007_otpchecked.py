# Generated by Django 5.0.2 on 2024-02-10 16:48

import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpChecked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Otp_code', models.CharField(max_length=6)),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_check_otp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
