# Generated by Django 4.2.7 on 2024-01-31 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='administracja',
            field=models.CharField(default=True, max_length=2),
        ),
    ]