# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-28 05:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi', '0021_auto_20161125_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmpdata',
            name='jsn',
            field=models.TextField(blank=True),
        ),
    ]