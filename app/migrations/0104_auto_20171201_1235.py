# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-01 04:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0103_auto_20170413_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access_hitory',
            name='referer',
            field=models.CharField(blank=True, max_length=5000),
        ),
    ]
