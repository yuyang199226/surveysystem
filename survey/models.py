from django.db import models
from rbac.models import User
# Create your models here.

class Survey(models.Model):
    '''问卷调查表'''
    title = models.CharField(max_length=64,verbose_name='问卷标题')
    theme = models.CharField(max_length=128,verbose_name='主题描述',blank=True,null=True)
    create_time = models.DateField(verbose_name='创建日期',auto_now_add=True)

    def __str__(self):
        return self.title



class Qitem(models.Model):
    '''问卷调查的项目'''
    CHOICE_TYPE = [
        ('single', '单选'),
        ('multi', '多选'),
        ('score', '评分1-10'),
        ('suggestion', '建议'),
    ]

    survey = models.ForeignKey(to='Survey',verbose_name='Q1',related_name='items')
    qcontent = models.CharField(verbose_name='问题',max_length=128)
    type = models.CharField(max_length=32,verbose_name='类型',choices=CHOICE_TYPE,default='single')

    def __str__(self):
        return self.qcontent

class ItemTypeDesc(models.Model):
    typedesc = models.CharField(max_length=64,verbose_name='内容',blank=True,null=True)
    score = models.IntegerField(verbose_name='分值',blank=True,null=True)
    item = models.ForeignKey(to=Qitem,verbose_name='问题')

class SurveyItemResult(models.Model):
    '''问卷调查的答案'''
    survey = models.ForeignKey(to=Survey,verbose_name='问卷')
    item = models.ForeignKey(to=Qitem,verbose_name='调查项')
    user = models.ForeignKey(to=User,verbose_name='回答者')

    single = models.ForeignKey(verbose_name='单选',to='ItemTypeDesc',blank=True,null=True)
    score = models.IntegerField(verbose_name='评分',blank=True,null=True)
    suggestion = models.TextField(verbose_name='建议',blank=True,null=True)

    date = models.DateField(verbose_name='回答日期',auto_now_add=True)

class Profile(models.Model):
    '''用户配置'''
    user = models.OneToOneField(to=User,verbose_name='用户')
    depart = models.ForeignKey(to='Department',verbose_name='部门')
    def __str__(self):
        return self.user.username

class Department(models.Model):
    '''部门表'''
    title = models.CharField(max_length=32,verbose_name='部门名')
    survey = models.OneToOneField(to='Survey', verbose_name='调查表',blank=True,null=True)
    def __str__(self):
        return self.title



