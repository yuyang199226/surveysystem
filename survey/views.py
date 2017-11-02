import json
from django.shortcuts import render,redirect,HttpResponse
from django.utils.safestring import mark_safe
from rbac import models as rbac_models
from . import forms
from . import models
import copy
from django.db import transaction

from django.http import QueryDict

class Survey(object):
    def __init__(self,survey_obj):
        self.survey = survey_obj
        self.items = survey_obj.items.all()
    def gen_item_html(self):
        items_html = ''
        print(self.items.count())
        for item in self.items:
            item_html = '<div>{}</div></hr>{}'.format(item.qcontent,
                                                          self.gen_type_html(item))
            items_html+=item_html
        return mark_safe(items_html)
    def gen_type_html(self,item_obj):
        item_type = item_obj.type
        html = getattr(self,item_type)(item_obj)
        return html

    def single(self,item_obj):
        '''生成单选框'''
        typedesces = item_obj.itemtypedesc_set.all()
        html = ''
        for i in typedesces:
            a = '<label><input type="radio" name={} value={}>{}</label></hr>'.format(item_obj.pk,i.score,i.typedesc)
            html+=a
        return html
    def suggestion(self,item_obj):
        '''建议'''
        html = '<textarea name={} id="" cols="60" rows="2" placeholder="请写下您宝贵的建议"></textarea>'.format(item_obj.pk)
        return html
        # types=['single','multi','score','suggestion']
        # for i in types:
    def multi(self,item_obj):
        '''多选'''
        typedesces = item_obj.itemtypedesc_set.all()
        html = ''
        for i in typedesces:
            a = '<label><input type="checkbox" name={} value={}>{}</label></hr>'.format(item_obj.pk, i.score, i.typedesc)
            html += a
        return html
    def score(self,item_obj):
        '''评分'''
        htmls = ''
        for i in range(1,11):
            html = '<label><input type="radio" name={} value={}><a class="btn btn-default btn-xs">i</a></label>'.format(item_obj.pk,i)
            htmls+=html
        return htmls





def login(request):
    if request.method == 'GET':
        loginform = forms.LoginForm()
        return render(request,'login.html',{'loginform':loginform})
    elif request.method == 'POST':
        loginform = forms.LoginForm(request.POST)
        if loginform.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = rbac_models.User.objects.filter(username=username,password=password)
            if user:
                return redirect('/home/')
            else:
                return render(request, 'login.html', {'loginform': loginform})
        else:
            return render(request,'login.html',{'loginform':loginform})

def survey_add(request):
    if request.method == 'GET':
        surveyform = forms.SurveyForm()
        qitemform = forms.QitemForm()
        typeform = forms.ItemTypeDescForm()
        context = {'surveyform':surveyform,
                   'qitemform':qitemform,
                   'typeform':typeform}
        return render(request,'survey_add.html',context)

    elif request.method == 'POST':
        surveyform = forms.SurveyForm(request.POST)
        try:
            with transaction.atomic():  #事务操作
                if surveyform.is_valid():
                    survey_obj = surveyform.save()
                    print(survey_obj.pk)
                    params = copy.deepcopy(request.POST)
                    params._mutable = True
                    del params['title']
                    del params['theme']
                    del params['csrfmiddlewaretoken']
                    dic = {}
                    for key in params:
                        name, num = key.split('-')
                        if num not in dic:
                            dic.setdefault(num, {})
                            temp = {name: params.getlist(key)}
                            dic[num].update(temp)

                        else:
                            temp = {name: params.getlist(key)}
                            dic[num].update(temp)
                    print(dic)
                    for num, dic_field in dic.items():
                        #{
                        # 0: {'qcontent':'dsa','type':'single','score':[10,5,2],'typedec':['aaa','bbb','ccc']}
                        # }
                        qitem_obj = models.Qitem(qcontent=dic_field['qcontent'][0],type=dic_field['type'][0],
                                     survey=survey_obj)
                        qitem_obj.save()

                        flag = dic_field['type'][0]
                        del dic_field['qcontent']
                        del dic_field['type']
                        print('>>>>>',dic_field)
                        if flag in ['single','multi']:
                            ls_all = []
                            for k, v in dic_field.items():
                                ls = []
                                for i in v:
                                    ls.append({k: i})
                                ls_all.append(ls)
                            for i in range(len(ls_all) - 1):
                                for j in range(len(ls_all[0])):
                                    ls_all[0][j].update(ls_all[i + 1][j])

                            # itemtype = list(zip(dic_field['typedesc'],dic_field['score']))
                            # print(itemtype)
                            for i in ls_all[0]:
                                type_obj = models.ItemTypeDesc(**i,item=qitem_obj)
                                type_obj.save()
        except Exception as e:
            return HttpResponse('出现错误')

        return redirect('/home/')

def home(request):
    surveies = models.Survey.objects.all()
    return render(request,'home.html',{'survies':surveies})

def questionsurvey(request,pk):
    survey_table_obj =models.Survey.objects.filter(pk=pk).first()
    #     .select_related('items').select_related('itemtypedesc_set')
    # for i in survey_table:
    #     print(i)

    survey_table = Survey(survey_table_obj)

    context = {
        'survey_table':survey_table
    }
    # print(survey_table2)
    return render(request,'survey_table.html',context)






def gen_survey_item(request):
    if request.is_ajax():
        qitemform = forms.QitemForm()
        htmls=''
        for field in qitemform:
            if not field.name == 'type':
                html = '<div class="form-group"><label>{}' \
                       '</label> <input class="" name="{}"></div>'.format(field.label,field.name)
                htmls+=html
            else:
                print(field.choices)
                # html = '<div class="form-group"><label>{}' \
                #        '</label> <input class="" name="{}"></div>'.format

    return HttpResponse(json.dumps('ok'))


