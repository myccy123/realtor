# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-19 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi', '0002_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='datais',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]