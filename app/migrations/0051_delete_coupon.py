# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-02 07:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_auto_20160902_1502'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Coupon',
        ),
    ]