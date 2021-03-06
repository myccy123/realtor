# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-02 00:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singlepage', '0035_auto_20180523_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing_for_sp',
            name='areas',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='basement',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='bedroom',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='builddate',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='cityname',
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='corp',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='goodat',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='housestyle',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='housetype',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='intro',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='listingid',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='listingname',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='parking',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='price',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='tax',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='toilet',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='listing_for_sp',
            name='warning',
            field=models.TextField(blank=True),
        ),
    ]
