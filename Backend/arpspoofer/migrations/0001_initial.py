# Generated by Django 5.1.2 on 2024-10-27 09:55

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Spoofer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spoofer_id', models.UUIDField(default=uuid.uuid4)),
                ('name', models.CharField(max_length=100)),
                ('target_ip', models.CharField(max_length=20)),
                ('target_mac', models.CharField(blank=True, max_length=20, null=True)),
                ('gateway_ip', models.CharField(max_length=20)),
                ('gateway_mac', models.CharField(blank=True, max_length=20, null=True)),
                ('total_count', models.IntegerField(blank=True, null=True)),
                ('time_ran', models.TimeField(blank=True, null=True)),
            ],
        ),
    ]
