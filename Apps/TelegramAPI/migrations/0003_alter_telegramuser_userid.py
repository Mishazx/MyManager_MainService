# Generated by Django 5.0.6 on 2024-06-29 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TelegramAPI', '0002_alter_telegramuser_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='userid',
            field=models.BigIntegerField(),
        ),
    ]