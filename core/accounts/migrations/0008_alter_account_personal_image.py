# Generated by Django 5.1.6 on 2025-03-25 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_account_date_of_birth_account_personal_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='personal_image',
            field=models.ImageField(upload_to='users_images/'),
        ),
    ]
