# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-01 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
        ('survey', '0003_auto_20171101_1310'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemTypeDesc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=64, verbose_name='类型内容')),
                ('score', models.IntegerField(verbose_name='分值')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyItemResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=128, verbose_name='调查结果')),
            ],
        ),
        migrations.RenameField(
            model_name='qitem',
            old_name='question',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='qitem',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='qitem',
            name='user',
        ),
        migrations.AddField(
            model_name='qitem',
            name='type',
            field=models.IntegerField(choices=[(0, '单选'), (1, '多选'), (2, '分数'), (3, '文本')], default=1, verbose_name='类型'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='survey',
            name='theme',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='主题描述'),
        ),
        migrations.AddField(
            model_name='surveyitemresult',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Qitem', verbose_name='问卷调查问题'),
        ),
        migrations.AddField(
            model_name='surveyitemresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rbac.User', verbose_name='回答者'),
        ),
        migrations.AddField(
            model_name='itemtypedesc',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Qitem', verbose_name='问题项目'),
        ),
    ]
