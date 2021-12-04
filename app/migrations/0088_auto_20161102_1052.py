# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-02 02:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0087_publish_apk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publish_apk',
            name='apkurl',
        ),
        migrations.AddField(
            model_name='publish_apk',
            name='apk',
            field=models.FileField(default='', upload_to='apks'),
        ),
    ]