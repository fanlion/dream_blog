# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-29 19:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_auto_20170929_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_source',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='来源'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=255, verbose_name='评论内容'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='home_url',
            field=models.URLField(blank=True, max_length=100, verbose_name='个人主页'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='nick_name',
            field=models.CharField(max_length=20, verbose_name='昵称'),
        ),
    ]
