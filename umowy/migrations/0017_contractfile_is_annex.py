# Generated by Django 4.2.7 on 2024-03-12 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umowy', '0016_delete_contractfileannex'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractfile',
            name='is_annex',
            field=models.BooleanField(default=False),
        ),
    ]
