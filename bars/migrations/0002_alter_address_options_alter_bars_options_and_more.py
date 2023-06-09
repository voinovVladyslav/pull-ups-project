# Generated by Django 4.2.1 on 2023-05-18 11:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bars', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'Address', 'verbose_name_plural': 'Addresses'},
        ),
        migrations.AlterModelOptions(
            name='bars',
            options={'verbose_name': 'Pull Up Bars', 'verbose_name_plural': 'Pull Up Bars'},
        ),
        migrations.AlterField(
            model_name='bars',
            name='longitude',
            field=models.DecimalField(decimal_places=8, max_digits=11, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)]),
        ),
    ]
