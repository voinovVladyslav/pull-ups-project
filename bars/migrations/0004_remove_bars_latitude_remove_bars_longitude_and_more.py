# Generated by Django 4.2.1 on 2023-05-31 17:25

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_alter_tag_name'),
        ('bars', '0003_bars_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bars',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='bars',
            name='longitude',
        ),
        migrations.AddField(
            model_name='bars',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='bars',
            name='tags',
            field=models.ManyToManyField(blank=True, to='tag.tag'),
        ),
    ]
