# Generated by Django 5.1.6 on 2025-03-05 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='first_name',
            field=models.CharField(default='null', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='last_name',
            field=models.CharField(default='null', max_length=30),
            preserve_default=False,
        ),
    ]
