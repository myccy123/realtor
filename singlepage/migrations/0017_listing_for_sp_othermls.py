# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-13 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singlepage', '0016_auto_20170813_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing_for_sp',
            name='othermls',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]