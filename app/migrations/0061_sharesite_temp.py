# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-21 02:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0060_custom_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharesite',
            name='temp',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
