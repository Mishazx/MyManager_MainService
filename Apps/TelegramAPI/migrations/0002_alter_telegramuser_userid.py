# Generated by Django 5.0.6 on 2024-06-29 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TelegramAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='userid',
            field=models.BigIntegerField(unique=True),
        ),
    ]
