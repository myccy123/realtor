# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-23 17:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singlepage', '0031_auto_20180514_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing_for_sp',
            name='distid',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
