# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-18 02:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0058_auto_20160918_1039'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Custom',
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
    ]