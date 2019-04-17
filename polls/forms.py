from django import forms
from django.contrib.auth.models import User

import re
from . import common

def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)

#岗位信息
class StationForm(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：UI设计师','class':'form-control'}))
    job_desc = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'描述岗位职责，要求等'}))
    edu_req = forms.CharField(widget=forms.Select(choices=(('1','不限'),('2','专科'),('3','本科'),('4','硕士'),('5','博士')),attrs={'class':'form-control'}))
    #exp_req = forms.CharField(widget=forms.Select(choices=(('1','无'),('2','一年'),('3','两年'),('4','三年及以上')),attrs={'class':'form-control'}))
    need = forms.IntegerField(label='', widget=forms.TextInput(attrs={'placeholder':'岗位人数需求','class':'form-control'}))
    city  = forms.CharField(widget=forms.Select(choices=common.city_choice,attrs={'class':'form-control selectpicker show-tick','data-live-search':'true'}))    
    #city = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：深圳','class':'form-control'}))
    salary1 = forms.IntegerField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：8000','class':'form-control'}))
    salary2 = forms.IntegerField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：8000','class':'form-control'}))
    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name
    def clean(self):
        cleaned_data = self.cleaned_data
        salary1 = cleaned_data['salary1']
        salary2 = cleaned_data['salary2']
        if salary1 <= 0 or salary2 <= 0:
            raise forms.ValidationError("salary can not be a negative.")
        elif salary1 > salary2:
            raise forms.ValidationError("invaile salary range.")
        return cleaned_data

#岗位信息过滤
class Job_filter(forms.Form):
    #就业城市过滤
    city_filter = forms.CharField(widget=forms.Select(choices=common.city_choice,attrs={'class':'selectpicker show-tick form-control','data-live-search':'true'}))
    #薪资过滤
    salary_filter = forms.CharField(widget=forms.Select(choices=common.salary_choice,attrs={'class':'selectpicker show-tick form-control','data-live-search':'true'}))

    #设置选中的城市
    def set_city(self,city):
        self.initial["city_filter"] = city
    #设置薪资要求
    def set_salary_req(self,sal):
        self.initial["salary_filter"] = sal        

#公司信息过滤
class Company_filter(forms.Form):
    #行业类型过滤
    type_filter = forms.CharField(widget=forms.Select(choices=common.ind_choice,attrs={'class':'selectpicker show-tick form-control','data-live-search':'true'}))
    #融资阶段过滤
    fin_filter  = forms.CharField(widget=forms.Select(choices=common.fin_choice,attrs={'class':'selectpicker show-tick form-control','data-live-search':'true'}))
    #公司规模过滤
    sca_filter  = forms.CharField(widget=forms.Select(choices=common.sca_choice,attrs={'class':'selectpicker show-tick form-control','data-live-search':'true'}))
    
    #设置选中的行业类型
    def set_type(self, type):
        self.initial["type_filter"] = type
    #设置选中的融资阶段
    def set_fin(self, fin):
        self.initial["fin_filter"] = fin
    #设置选中的公司规模
    def set_scale(self, sca):
        self.initial["sca_filter"] = sca

#教育经历表单
class EduForm(forms.Form):
    school = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：北京大学','class':'form-control'}))
    pro = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：计算机科学与技术','class':'form-control'}))
    start_date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control','type':'text','value':'','readonly':'True'},format='%d/%m/%Y'))
    end_date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control','type':'text','value':'','readonly':'True'},format='%d/%m/%Y'))
    edu = forms.ChoiceField(label='',choices=(('0','-----'),('1','专科'),('2','本科'),('3','硕士'),('4','博士')),widget=forms.Select(attrs={'class':'form-control'}))

    def clean_school(self):
        school = self.cleaned_data.get('school')
        return school

#项目经历
class ProForm(forms.Form):
    job_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：直聘网','class':'form-control'}))
    job_role = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：UI设计师','class':'form-control'}))
    start_date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control','type':'text','value':'','readonly':'True'},format='%d/%m/%Y'))
    end_date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control','type':'text','value':'','readonly':'True'},format='%d/%m/%Y'))
    job_desc = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'描述该项目，向BOSS展示你的项目经验\n例如：\n1.项目概述...\n2.人员分工...\n3.我的责任...'}))

    def clean_school(self):
        job_name = self.cleaned_data.get('job_name')
        return job_name

#工作经历
class JobForm(forms.Form):
    start_date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control','type':'text','value':'','readonly':'True'},format='%d/%m/%Y'))
    end_date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control','type':'text','value':'','readonly':'True'},format='%d/%m/%Y'))
    company_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：深信服科技股份有限公司','class':'form-control'}))
    job_role = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：C++开发工程师','class':'form-control'}))
    job_desc = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'例如：\n1.主要负责新员工入职员工培训；\n2.分析制定员工每个月个人销售业绩；\n3.帮助员工提高每日客单价，整体店面等工作；'}))
    industry = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：互联网','class':'form-control'}))

    def clean_industry(self):
        industry = self.cleaned_data.get('industry')
        return industry

#学生注册
class StuRegisterForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder':'','required':'','class':'name','type':'text','name':'name'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder':'','required':'','class':'password','type':'password','name':'password'}))
    comfirm_passwd = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder':'','required':'','class':'password','type':'password','name':'password'}))
    email = forms.CharField(label='', widget=forms.TextInput(
         attrs={'placeholder':'','required':'','class':'name','type':'text','name':'email'}))
    
    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')
        filter_result = User.objects.filter(username__exact=username)
        if filter_result.count() > 0:
            raise forms.ValidationError("用户名已存在!")
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        right = False
        if len(email) > 7:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                right=True
        if not right:
            raise forms.ValidationError('请输入合法的邮箱！')
        return email 

    def clean(self):
        cleaned_data = self.cleaned_data
        pwd1 = cleaned_data['password']
        pwd2 = cleaned_data['comfirm_passwd']
        #print(pwd1,pwd2)
        if pwd1 != pwd2:
            raise forms.ValidationError('二次输入密码不匹配!')    
        return cleaned_data 

#企业注册
class ComRegisterForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder':'','required':'','class':'name','type':'text','name':'name'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder':'','required':'','class':'password','type':'password','name':'password'}))
    comfirm_passwd = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder':'','required':'','class':'password','type':'password','name':'password'}))
    email = forms.CharField(label='', widget=forms.TextInput(
         attrs={'placeholder':'','required':'','class':'name','type':'text','name':'email'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        filter_result = User.objects.filter(username__exact=username)
        if filter_result.count() > 0:
            raise forms.ValidationError("用户名已存在!")
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        right = False
        if len(email) > 7:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                right=True
        if not right:
            raise forms.ValidationError('请输入合法的邮箱！')
        return email 

    def clean(self):
        cleaned_data = self.cleaned_data
        pwd1 = cleaned_data['password']
        pwd2 = cleaned_data['comfirm_passwd']
        #print(pwd1,pwd2)
        if pwd1 != pwd2:
            raise forms.ValidationError('二次输入密码不匹配!')    
        return cleaned_data 

#登陆
class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder':'','required':'','class':'name','type':'text','name':'name'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder':'','required':'','class':'password','type':'password','name':'password'}))

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data['username']
        password = cleaned_data['password']
        filter_result = User.objects.filter(username__exact=username)
        if filter_result.count() > 0:
            if not filter_result[0].check_password(password):
                raise forms.ValidationError("用户名或密码错误！")
        else:
            raise forms.ValidationError("用户名不存在，请先注册！")
        return cleaned_data
