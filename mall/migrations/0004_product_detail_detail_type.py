# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-13 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0003_product_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_detail',
            name='detail_type',
            field=models.CharField(choices=[('txt', '\u6587\u5b57'), ('img', '\u56fe\u7247')], default='txt', max_length=500),
        ),
    ]