# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-29 06:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi', '0008_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='temptype',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
