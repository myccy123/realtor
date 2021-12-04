# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-21 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi', '0024_source_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='source_file',
            name='hashead',
            field=models.CharField(blank=True, max_length=1),
        ),
        migrations.AlterField(
            model_name='source_file',
            name='file',
            field=models.FileField(blank=True, upload_to='srcfile'),
        ),
        migrations.AlterField(
            model_name='source_file',
            name='filetype',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='source_file',
            name='sourceid',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
