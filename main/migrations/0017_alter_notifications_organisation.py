# Generated by Django 4.2 on 2023-06-09 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_user_phone'),
        ('main', '0016_alter_images_organisation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organisation_notifications', to='accounts.organisations'),
        ),
    ]
