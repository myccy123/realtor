# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-06 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_listingimg_imgtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='agentid',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='assistanttel',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='creaid',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='assistant',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='corpintro',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='note',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='selfintro',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='siteurl',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='teamintro',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='tel',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='usercity',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='warning',
            field=models.TextField(blank=True),
        ),
    ]