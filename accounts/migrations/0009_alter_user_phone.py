# Generated by Django 4.2 on 2023-05-04 20:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=200, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+2341234567890'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='phone'),
        ),
    ]
