# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-09 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FriendCorp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('corp_url', models.CharField(max_length=100)),
                ('logo', models.FileField(blank=True, upload_to='corps')),
                ('qr_code', models.FileField(blank=True, upload_to='corps')),
            ],
            options={
                'verbose_name': '\u5408\u4f5c\u5730\u4ea7\u516c\u53f8',
                'verbose_name_plural': '\u5408\u4f5c\u5730\u4ea7\u516c\u53f8',
            },
        ),
    ]