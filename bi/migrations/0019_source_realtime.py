# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-25 06:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi', '0018_auto_20161125_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='realtime',
            field=models.CharField(blank=True, max_length=1),
        ),
    ]
