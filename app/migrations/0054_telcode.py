# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-06 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_auto_20160902_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='Telcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel', models.CharField(max_length=100)),
                ('vcode', models.CharField(max_length=6)),
            ],
        ),
    ]
