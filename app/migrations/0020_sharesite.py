# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20160721_2158'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sharesite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('htmlid', models.CharField(max_length=100)),
                ('userid', models.CharField(max_length=100)),
                ('infoid', models.CharField(max_length=100)),
                ('sharetype', models.CharField(max_length=30)),
                ('sharetime', models.CharField(max_length=30)),
                ('htmlfile', models.FileField(upload_to='htmls')),
            ],
        ),
    ]
