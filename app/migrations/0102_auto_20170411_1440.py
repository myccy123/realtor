# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-11 06:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0101_auto_20170327_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='lat',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='listing',
            name='lng',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='listing',
            name='postid',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
