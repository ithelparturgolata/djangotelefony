# Generated by Django 4.2.7 on 2024-01-27 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telefony', '0004_phonenumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blok',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol_budynku', models.CharField(max_length=255)),
                ('adres_budynku', models.CharField(max_length=255)),
                ('administracja', models.CharField(max_length=2, null=True)),
            ],
        ),
    ]