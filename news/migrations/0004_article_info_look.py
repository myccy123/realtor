# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-03 15:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20161207_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='article_info',
            name='look',
            field=models.IntegerField(default=0),
        ),
    ]