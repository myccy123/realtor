# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-07 14:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20161207_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article_content',
            name='img',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news.Article_img'),
        ),
        migrations.AlterField(
            model_name='article_img',
            name='img',
            field=models.FileField(upload_to=b'articleimg'),
        ),
    ]
