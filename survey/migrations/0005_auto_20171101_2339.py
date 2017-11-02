# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-01 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20171101_2030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qitem',
            old_name='content',
            new_name='qcontent',
        ),
        migrations.RemoveField(
            model_name='itemtypedesc',
            name='content',
        ),
        migrations.AddField(
            model_name='itemtypedesc',
            name='typedesc',
            field=models.CharField(default=1, max_length=64, verbose_name='内容'),
            preserve_default=False,
        ),
    ]