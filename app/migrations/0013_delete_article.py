# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 12:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_article'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Article',
        ),
    ]