# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-21 03:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi', '0005_tmpdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_data',
            name='data',
            field=models.FileField(upload_to='chartdata'),
        ),
    ]
