# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-14 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0019_auto_20190711_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='email_list',
            name='mls',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='email_list',
            name='userid',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
