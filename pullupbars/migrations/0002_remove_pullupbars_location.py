# Generated by Django 4.2.1 on 2024-03-18 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pullupbars', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pullupbars',
            name='location',
        ),
    ]
