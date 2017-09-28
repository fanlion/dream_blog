# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-30 20:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0027_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建日期'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='visitrecord',
            name='server_name',
            field=models.CharField(max_length=40, verbose_name='server_name'),
        ),
    ]