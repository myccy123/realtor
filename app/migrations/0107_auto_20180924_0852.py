# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-24 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0106_auto_20180331_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access_hitory',
            name='htmltype',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]