# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-01 02:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0082_auto_20161101_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='system_msg',
            name='msgstatus',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
