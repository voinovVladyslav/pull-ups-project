# Generated by Django 4.2.1 on 2024-03-18 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training_ground', '0003_trainingground_dipstation_and_more'),
        ('dipstations', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DipStation',
            new_name='DipStations',
        ),
    ]