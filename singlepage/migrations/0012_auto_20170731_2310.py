# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-31 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singlepage', '0011_listing_for_sp_titleagent'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing_for_sp',
            name='salestatus',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='url',
            field=models.CharField(blank=True, max_length=5000),
        ),
    ]
