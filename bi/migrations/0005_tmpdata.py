# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-19 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi', '0004_auto_20160719_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tmpdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.FileField(upload_to='tmp')),
            ],
        ),
    ]
