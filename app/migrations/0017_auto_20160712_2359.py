# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 15:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_listings_intro_eng'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Listings',
            new_name='Listing',
        ),
    ]