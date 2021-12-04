# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-18 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_auto_20160818_1134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.FileField(upload_to='ad')),
                ('url', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
