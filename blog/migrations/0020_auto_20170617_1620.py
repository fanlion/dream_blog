# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-17 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_auto_20170616_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitstatistics',
            name='today_visit',
            field=models.PositiveIntegerField(default=0, verbose_name='访问量'),
        ),
    ]
