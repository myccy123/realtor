# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-30 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_agent_auth_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent_auth',
            name='invoice',
            field=models.FileField(blank=True, upload_to='invoices'),
        ),
    ]