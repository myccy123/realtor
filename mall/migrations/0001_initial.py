# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-10 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wechat_user_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=50)),
                ('nickname', models.CharField(blank=True, max_length=100)),
                ('headimgurl', models.CharField(blank=True, max_length=1000)),
                ('sex', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('province', models.CharField(blank=True, max_length=100)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('language', models.CharField(blank=True, max_length=100)),
                ('logindate', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u5fae\u4fe1\u7528\u6237\u4fe1\u606f',
                'verbose_name_plural': '\u5fae\u4fe1\u7528\u6237\u4fe1\u606f',
            },
        ),
    ]
