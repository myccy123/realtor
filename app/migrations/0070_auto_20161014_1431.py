# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-14 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0069_auto_20161013_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wechat_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unionid', models.DateTimeField(blank=True, max_length=100)),
                ('openid', models.CharField(blank=True, max_length=100)),
                ('nickname', models.CharField(blank=True, max_length=100)),
                ('sex', models.CharField(blank=True, max_length=100)),
                ('province', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('country', models.DateTimeField(blank=True, max_length=100)),
                ('headimgurl', models.DateTimeField(blank=True, max_length=100)),
                ('privilege', models.DateTimeField(blank=True, max_length=100)),
                ('datadate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='wechatid',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]