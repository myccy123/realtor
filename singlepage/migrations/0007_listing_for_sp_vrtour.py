# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-19 05:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singlepage', '0006_auto_20170715_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing_for_sp',
            name='vrtour',
            field=models.TextField(blank=True),
        ),
    ]
