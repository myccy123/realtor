# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-22 21:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0021_auto_20190811_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent_img',
            name='imgtype',
            field=models.CharField(blank=True, choices=[('agent', '\u7ecf\u7eaa\u7167\u7247'), ('corp', '\u516c\u53f8\u7167\u7247'), ('video', '\u7ecf\u7eaa\u89c6\u9891'), ('emaillist', '\u90ae\u4ef6\u5217\u8868\uff08Excel\uff09')], max_length=100),
        ),
    ]