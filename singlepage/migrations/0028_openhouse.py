# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-02 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singlepage', '0027_auto_20180114_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='Openhouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listingid', models.CharField(max_length=50)),
                ('opendate1', models.DateTimeField(blank=True)),
                ('opendate2', models.DateTimeField(blank=True)),
            ],
            options={
                'verbose_name': '\u516c\u4f17\u5f00\u653e\u65e5',
                'verbose_name_plural': '\u516c\u4f17\u5f00\u653e\u65e5',
            },
        ),
    ]
