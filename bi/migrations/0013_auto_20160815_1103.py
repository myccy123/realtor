# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-15 03:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi', '0012_auto_20160805_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_data',
            name='datatype',
            field=models.CharField(blank=True, default='9', max_length=50),
        ),
    ]