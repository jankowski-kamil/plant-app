# Generated by Django 4.2.13 on 2024-06-13 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0005_rename_watering_waterings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Waterings',
            new_name='Watering',
        ),
    ]