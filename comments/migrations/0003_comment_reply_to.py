# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-10 09:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20170709_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply_to',
            field=models.ManyToManyField(related_name='_comment_reply_to_+', to='comments.Comment', verbose_name='回复'),
        ),
    ]
