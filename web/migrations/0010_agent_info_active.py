# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-24 10:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20180512_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent_info',
            name='active',
            field=models.CharField(default='1', max_length=10),
        ),
    ]
