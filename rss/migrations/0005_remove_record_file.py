# Generated by Django 4.2.7 on 2024-03-22 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0004_rename_recordrss_record'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='file',
        ),
    ]