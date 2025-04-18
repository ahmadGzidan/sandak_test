# Generated by Django 5.1.6 on 2025-04-18 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_account_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='gender',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='account',
            name='personal_image',
            field=models.ImageField(blank=True, null=True, upload_to='users_images/'),
        ),
    ]
