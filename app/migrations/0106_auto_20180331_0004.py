# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-30 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0105_auto_20180319_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='datadate',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
