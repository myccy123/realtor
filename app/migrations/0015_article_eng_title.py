# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='eng_title',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
