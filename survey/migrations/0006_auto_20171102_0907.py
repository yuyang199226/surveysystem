# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-02 01:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_auto_20171101_2339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyitemresult',
            name='answer',
        ),
        migrations.AddField(
            model_name='surveyitemresult',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='回答日期'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='surveyitemresult',
            name='score',
            field=models.IntegerField(default=1, verbose_name='评分'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='surveyitemresult',
            name='single',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.ItemTypeDesc', verbose_name='单选'),
        ),
        migrations.AddField(
            model_name='surveyitemresult',
            name='suggestion',
            field=models.TextField(blank=True, null=True, verbose_name='建议'),
        ),
        migrations.AddField(
            model_name='surveyitemresult',
            name='survey',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='survey.Survey', verbose_name='问卷'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='itemtypedesc',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Qitem', verbose_name='问题'),
        ),
        migrations.AlterField(
            model_name='qitem',
            name='type',
            field=models.CharField(choices=[('single', '单选'), ('multi', '多选'), ('score', '评分'), ('suggestion', '建议')], default='single', max_length=32, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='surveyitemresult',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Qitem', verbose_name='调查项'),
        ),
    ]
