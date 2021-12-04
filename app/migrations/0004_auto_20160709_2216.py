# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_listingimgs_listings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listingimgs',
            name='id',
        ),
        migrations.RemoveField(
            model_name='listings',
            name='id',
        ),
        migrations.AddField(
            model_name='listingimgs',
            name='imgname',
            field=models.CharField(blank=True, max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='listings',
            name='listingid',
            field=models.CharField(blank=True, max_length=50, primary_key=True, serialize=False),
        ),
    ]
