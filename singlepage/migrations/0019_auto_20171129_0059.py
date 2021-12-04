# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-28 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singlepage', '0018_order_from_website'),
    ]

    operations = [
        migrations.CreateModel(
            name='BI_map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mls', models.CharField(blank=True, max_length=20)),
                ('token', models.CharField(blank=True, max_length=50)),
                ('template_id', models.CharField(blank=True, max_length=50)),
                ('orderid', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='sp_img',
            name='imgtype',
            field=models.CharField(choices=[('hx', '\u6237\u578b\u56fe'), ('video', '\u89c6\u9891'), ('pdf', 'PDF'), ('bgimg1', '\u7b2c\u4e00\u5e45\u80cc\u666f\u56fe'), ('bgimg2', '\u7b2c\u4e8c\u5e45\u80cc\u666f\u56fe'), ('bgimg3', '\u7b2c\u4e09\u5e45\u80cc\u666f\u56fe'), ('bgimg4', '\u7b2c\u56db\u5e45\u80cc\u666f\u56fe'), ('preimg', '\u7f29\u7565\u56fe')], max_length=100),
        ),
    ]
