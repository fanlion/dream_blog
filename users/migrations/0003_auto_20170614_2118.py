# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-14 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170607_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=50, verbose_name='昵称'),
        ),
    ]
