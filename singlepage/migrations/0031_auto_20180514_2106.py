# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-14 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singlepage', '0030_auto_20180514_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openhouse',
            name='bgndate1',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='openhouse',
            name='bgndate2',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='openhouse',
            name='enddate1',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='openhouse',
            name='enddate2',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
