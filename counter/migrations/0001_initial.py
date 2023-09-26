# Generated by Django 4.2.1 on 2023-07-21 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bars', '0005_alter_bars_location'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PullUpCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reps', models.PositiveIntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('bar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pullup_counter', to='bars.bars')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pullup_counter', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]