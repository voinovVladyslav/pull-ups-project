# Generated by Django 4.2.1 on 2024-03-16 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bars', '0006_alter_bars_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bars',
            name='address',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]