# Generated by Django 4.2.1 on 2024-03-16 10:59

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('bars', '0001_initial'), ('bars', '0002_alter_address_options_alter_bars_options_and_more'), ('bars', '0003_bars_tags'), ('bars', '0004_remove_bars_latitude_remove_bars_longitude_and_more'), ('bars', '0005_alter_bars_location'), ('bars', '0006_alter_bars_address'), ('bars', '0007_remove_bars_address_delete_address'), ('bars', '0008_remove_bars_tags')]

    initial = True

    # dependencies = [
    #     ('tag', '0001_initial'),
    #     ('tag', '0002_alter_tag_name'),
    # ]

    operations = [
        migrations.CreateModel(
            name='Bars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326)),
            ],
            options={
                'verbose_name': 'Pull Up Bars',
                'verbose_name_plural': 'Pull Up Bars',
            },
        ),
    ]