# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-13 08:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0068_custom_notes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='custom',
            options={'verbose_name': '\u79c1\u4eba\u8ba2\u5236', 'verbose_name_plural': '\u79c1\u4eba\u8ba2\u5236'},
        ),
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': '\u95ee\u9898\u53cd\u9988', 'verbose_name_plural': '\u95ee\u9898\u53cd\u9988'},
        ),
        migrations.AlterModelOptions(
            name='systemorder',
            options={'verbose_name': '\u7cfb\u7edf\u8ba2\u5355', 'verbose_name_plural': '\u7cfb\u7edf\u8ba2\u5355'},
        ),
    ]