import json
from django.shortcuts import render,redirect,HttpResponse
from django.utils.safestring import mark_safe
from rbac import models as rbac_models
from . import forms
from . import models
import copy
from django.db import transaction



class Survey(object):

    def __init__(self,survey_obj):
        self.survey = survey_obj
        self.items = survey_obj.items.all()

    def gen_item_html(self):
        items_html = '<div class="item-area">'
        print(self.items.count())
        for item in self.items:
            item_html = '<div class="item-title">{}</div class="item-body"><div>{}</div>'.format(item.qcontent,
                                                          self.gen_type_html(item))
            items_html+=item_html
        items_html+='</div>'
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
            name = '{}/{}'.format(item_obj.pk,'single')
            a = '<label><input type="radio" name={} value={}>{}</label></hr>'.format(name,i.pk,i.typedesc)
            html+=a

        return html

    def multi(self,item_obj):
        '''多选'''
        typedesces = item_obj.itemtypedesc_set.all()
        html = ''
        for i in typedesces:
            name='{}/{}'.format(item_obj.pk,'multi')
            a = '<label><input type="checkbox" name={} value={}>{}</label></hr>'.format(name, i.pk, i.typedesc)
            html += a
        return html

    def suggestion(self,item_obj):
        '''建议'''
        name = '{}/{}'.format(item_obj.pk,'suggestion')
        html = '<textarea name={} id="" cols="60" rows="2" placeholder="请写下您宝贵的建议"></textarea>'.format(name)
        return html

    def score(self,item_obj):
        '''评分'''
        htmls = ''
        for i in range(1,11):
            name='{}/{}'.format(item_obj.pk,'score')
            html = ' <label><input type="radio" name={} value={}><a class="btn btn-default btn-xs">{}</a></label> '.format(name,i,i)
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
                request.session['userinfo']= user.first().pk #加到session中
                return redirect('/home/')
            else:
                return render(request, 'login.html', {'loginform': loginform})
        else:
            return render(request,'login.html',{'loginform':loginform})

def survey_add(request):
    '''创建一张调查问卷'''
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
    '''提交问卷'''
    if request.method == 'GET':
        survey_table_obj =models.Survey.objects.filter(pk=pk).first()
        survey_table = Survey(survey_table_obj)
        context = {
            'survey_table':survey_table
        }
        return render(request,'survey_table.html',context)

    elif request.method == 'POST':
        survey_pk = pk
        user_pk = request.session.get('userinfo')
        print(user_pk)
        flag = models.SurveyItemResult.objects.filter(user=user_pk)
        if flag:
            return HttpResponse('不能重复提交')
        params = copy.deepcopy(request.POST)
        params._mutable = True
        del params['csrfmiddlewaretoken']
        for name,value in params.items():
            # try:
            #     with transaction.atomic():
            item_obj_pk,type = name.split('/')
            if type == 'single':
                single_id = params.get(name).strip()
                models.SurveyItemResult.objects.create(survey_id=survey_pk,item_id=item_obj_pk, user_id=user_pk,single_id=int(single_id))

            elif type == 'multi':
                multi_ids = params.getlist(name)
                for id in multi_ids:
                    models.SurveyItemResult.objects. \
                        create(survey_id=survey_pk, item_id=item_obj_pk, user_id=user_pk,
                               single_id=int(id))

            elif type == 'score':
                models.SurveyItemResult.objects. \
                    create(survey_id=survey_pk, item_id=item_obj_pk, user_id=user_pk,
                           score=int(params.get(name)))

            else:
                models.SurveyItemResult.objects. \
                    create(survey_id=survey_pk, item_id=item_obj_pk, user_id=user_pk,
                           suggestion=params.get(name))
            # except Exception as e:
            #     return HttpResponse('提交失败了')

        print('>>>>>>',request.POST)
        return HttpResponse('提交成功')

def surveydelete(request,pk):
    # '''删除问卷调查'''
   try:
        models.Survey.objects.filter(pk=pk).delete()
        return redirect('/home/')
   except Exception as e:
        return HttpResponse('删除失败')

def surveyresult(request,pk):
    '''调查问卷的页面展示'''
    survey_obj = models.Survey.objects.get(pk=pk)
    survey_questions= survey_obj.items.all()
    survey_results = models.SurveyItemResult.objects.filter(survey_id=pk)
    num = (survey_results.count())//(survey_questions.count()) #不准确
    context = {
        'survey_obj':survey_obj,
        'survey_questions':survey_questions,
        'survey_results':survey_results,
        'num':num,
    }
    for question in survey_questions:
        pass
    return render(request,'survey/survey_report.html',context)
def multi_data(request):
    '''显示多选图表,，返回图表所需数据'''
    pk = request.GET.get('pk')
    question = models.Qitem.objects.get(pk=pk)
    x_list = [i.typedesc for i in question.itemtypedesc_set.all()]
    y_list = [0 for i in range(len(x_list))]
    results = question.surveyitemresult_set.all()
    for result_obj in results:
        for ix in range(len(x_list)):
            if result_obj.single.typedesc == x_list[ix]:
                y_list[ix]+=1
    data = {'x':x_list,'y':y_list}
    return  HttpResponse(json.dumps(data))

def single_data(request):
    ''',返回单选图表所需数据'''
    pk = request.GET.get('pk')
    question = models.Qitem.objects.get(pk=pk)
    x_list = [i.typedesc for i in question.itemtypedesc_set.all()]
    y_list = [0 for i in range(len(x_list))]
    results = question.surveyitemresult_set.all()
    for result_obj in results:
        for ix in range(len(x_list)):
            if result_obj.single.typedesc == x_list[ix]:
                y_list[ix] += 1
    data=[]
    for i in range(len(x_list)):
        data.append({'value':y_list[i],'name':x_list[i]})
    return HttpResponse(json.dumps(data))






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


