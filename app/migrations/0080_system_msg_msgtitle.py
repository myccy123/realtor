# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-28 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0079_system_msg'),
    ]

    operations = [
        migrations.AddField(
            model_name='system_msg',
            name='msgtitle',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]