# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-02 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singlepage', '0037_auto_20180902_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing_for_sp',
            name='sptype',
            field=models.CharField(blank=True, default='smf', max_length=100),
        ),
    ]
