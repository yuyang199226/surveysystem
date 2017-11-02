from django import forms
from rbac import models as rbac_models
from survey import models as survey_models
class LoginForm(forms.ModelForm):
    class Meta:
        model = rbac_models.User
        fields = ['username','password']
        widgets = {
            'password':forms.PasswordInput(
                attrs={'name':'password','placeholder':'密码'}),
            'username':forms.TextInput(
                attrs={'name':'username','placeholder':'用户名'},
            )
        }

class SurveyForm(forms.ModelForm):
    class Meta:
        model = survey_models.Survey
        fields = ['title','theme']

class QitemForm(forms.ModelForm):
    class Meta:
        model = survey_models.Qitem
        fields = ['qcontent','type']
        # widgets = {
        #     'content': forms.PasswordInput(
        #         attrs={'name': 'content', 'placeholder': '问题描述'}),
        #     'username': forms.choi(
        #         attrs={'name': 'username', 'placeholder': '用户名'},
        #     )
        # }

class ItemTypeDescForm(forms.ModelForm):
    class Meta:
        model = survey_models.ItemTypeDesc
        fields = ['typedesc','score']

