# Generated by Django 4.2.13 on 2024-06-13 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0004_watering_litres'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Watering',
            new_name='Waterings',
        ),
    ]