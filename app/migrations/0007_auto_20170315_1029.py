# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-15 07:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20170311_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 15, 10, 29, 4, 952720)),
        ),
        migrations.AlterField(
            model_name='user',
            name='telegram_id',
            field=models.CharField(default='', max_length=15, unique=True),
        ),
    ]
