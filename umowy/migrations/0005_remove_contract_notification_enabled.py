# Generated by Django 4.2.7 on 2024-02-15 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umowy', '0004_contract_notification_enabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='notification_enabled',
        ),
    ]