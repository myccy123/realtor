# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-02 03:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0088_auto_20161102_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='publish_apk',
            name='versioncode',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]