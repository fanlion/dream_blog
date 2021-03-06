# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-17 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_blacklist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacklist',
            name='deny_reason',
            field=models.CharField(choices=[('1', '爬虫'), ('2', '破解密码'), ('3', '不友好用户')], default='1', max_length=20, verbose_name='禁止原因'),
        ),
        migrations.AlterField(
            model_name='blacklist',
            name='ip',
            field=models.CharField(max_length=20, unique=True, verbose_name='ip地址'),
        ),
    ]
