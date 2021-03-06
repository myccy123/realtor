# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-16 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_sharesite_comm'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharesite',
            name='translated',
            field=models.CharField(default='0', max_length=1),
        ),
        migrations.AddField(
            model_name='systemorder',
            name='dataid',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='systemorder',
            name='ordertype',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='systemorder',
            name='transid',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='bal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16),
        ),
    ]
