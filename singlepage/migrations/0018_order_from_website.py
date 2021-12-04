# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-18 06:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singlepage', '0017_listing_for_sp_othermls'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_from_website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(blank=True, max_length=100)),
                ('lname', models.CharField(blank=True, max_length=100)),
                ('email', models.CharField(blank=True, max_length=100)),
                ('mls', models.CharField(blank=True, max_length=100)),
                ('tel', models.CharField(blank=True, max_length=100)),
                ('corp', models.CharField(blank=True, max_length=500)),
                ('address', models.CharField(blank=True, max_length=500)),
                ('postid', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]