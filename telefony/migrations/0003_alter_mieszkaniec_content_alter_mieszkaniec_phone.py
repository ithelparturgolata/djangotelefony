# Generated by Django 4.2.7 on 2023-12-08 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telefony', '0002_alter_mieszkaniec_data_utworzenia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mieszkaniec',
            name='content',
            field=models.TextField(blank=True, max_length=160, null=True),
        ),
        migrations.AlterField(
            model_name='mieszkaniec',
            name='phone',
            field=models.TextField(blank=True, max_length=9, null=True),
        ),
    ]