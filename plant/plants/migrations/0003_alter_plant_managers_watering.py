# Generated by Django 4.2.13 on 2024-06-13 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0002_alter_plant_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='plant',
            managers=[
            ],
        ),
        migrations.CreateModel(
            name='Watering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watering_date', models.DateField()),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watering', to='plants.plant')),
            ],
        ),
    ]