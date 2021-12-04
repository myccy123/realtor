# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_delete_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False)),
                ('article_type', models.CharField(blank=True, max_length=50)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('pro', models.CharField(blank=True, max_length=2000)),
                ('img_url', models.CharField(blank=True, max_length=200)),
                ('article_url', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
