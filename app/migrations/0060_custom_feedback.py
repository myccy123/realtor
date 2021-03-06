# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-18 02:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0059_auto_20160918_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Custom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cityname', models.CharField(blank=True, max_length=100)),
                ('bedroom', models.CharField(blank=True, max_length=100)),
                ('toilet', models.CharField(blank=True, max_length=100)),
                ('userid', models.CharField(blank=True, max_length=100)),
                ('username', models.CharField(blank=True, max_length=100)),
                ('usercity', models.CharField(blank=True, max_length=100)),
                ('tel', models.CharField(blank=True, max_length=100)),
                ('pricezone', models.CharField(blank=True, max_length=100)),
                ('buydate', models.CharField(blank=True, max_length=100)),
                ('addservice', models.CharField(blank=True, max_length=100)),
                ('datadate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(blank=True, max_length=100)),
                ('problem', models.CharField(blank=True, max_length=2000)),
                ('idea', models.CharField(blank=True, max_length=2000)),
                ('tel', models.CharField(blank=True, max_length=100)),
                ('email', models.CharField(blank=True, max_length=100)),
                ('datadate', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
