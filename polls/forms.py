from django import forms
from django.contrib.auth.models import User
import re


def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)

#岗位信息
class StationForm(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：UI设计师','class':'form-control'}))
    job_desc = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'描述岗位职责，要求等'}))
    edu_req = forms.CharField(widget=forms.Select(choices=(('1','不限'),('2','专科'),('3','本科'),('4','硕士'),('5','博士')),attrs={'class':'form-control'}))
    exp_req = forms.CharField(widget=forms.Select(choices=(('1','无'),('2','一年'),('3','两年'),('4','三年及以上')),attrs={'class':'form-control'}))
    city = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：深圳','class':'form-control'}))
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
        

#教育经历表单
class EduForm(forms.Form):
    school = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：北京大学','class':'form-control'}))
    pro = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：计算机科学与技术','class':'form-control'}))
    start_date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control'},format='%d/%m/%Y'))
    end_date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control'},format='%d/%m/%Y'))
    edu = forms.ChoiceField(label='',choices=(('0','-----'),('1','专科'),('2','本科'),('3','硕士'),('4','博士')),widget=forms.Select(attrs={'class':'form-control'}))

    def clean_school(self):
        school = self.cleaned_data.get('school')
        return school

#项目经历
class ProForm(forms.Form):
    job_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：直聘网','class':'form-control'}))
    job_role = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：UI设计师','class':'form-control'}))
    start_date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control'},format='%d/%m/%Y'))
    end_date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control'},format='%d/%m/%Y'))
    job_desc = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'描述该项目，向BOSS展示你的项目经验\n例如：\n1.项目概述...\n2.人员分工...\n3.我的责任...'}))

    def clean_school(self):
        job_name = self.cleaned_data.get('job_name')
        return job_name

#工作经历
class JobForm(forms.Form):
    start_date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control'},format='%d/%m/%Y'))
    end_date = forms.DateField(label='', widget=forms.DateInput(attrs={'class':'form-control'},format='%d/%m/%Y'))
    company_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：深信服科技股份有限公司','class':'form-control'}))
    job_role = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：C++开发工程师','class':'form-control'}))
    job_desc = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'例如：\n1.主要负责新员工入职员工培训；\n2.分析制定员工每个月个人销售业绩；\n3.帮助员工提高每日客单价，整体店面等工作；'}))
    industry = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'例如：互联网','class':'form-control'}))

    def clean_industry(self):
        industry = self.cleaned_data.get('industry')
        return industry

#学生注册
class StuRegisterForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'用户名','class':'lowin-input'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'密码','class':'lowin-input'}))
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'邮箱','class':'lowin-input'}))
    phone = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'手机','class':'lowin-input'}))
    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6:
            raise forms.ValidationError("Your username must be at least 6 characters long.")
        elif len(username) > 50:
            raise forms.ValidationError("Your username is too long.")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your username already exists.")
        return username
    """
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your email already exists.")
            else:
                raise forms.ValidationError("Please enter a valid email.")
        return email
    """
    """
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 6:
            raise forms.ValidationError("Your password is too short.")
        elif len(password) > 20:
            raise forms.ValidationError("Your password is too long.")

        return password
    """
#企业注册
class ComRegisterForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'用户名','class':'lowin-input'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'密码','class':'lowin-input'}))
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'邮箱','class':'lowin-input'}))
    phone = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'手机','class':'lowin-input'}))
    #company = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'企业','class':'lowin-input'}))
    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6:
            raise forms.ValidationError("Your username must be at least 6 characters long.")
        elif len(username) > 50:
            raise forms.ValidationError("Your username is too long.")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your username already exists.")
        return username

    def clean_com_name(self):
        company = self.cleaned_data.get('company')
        return company

#登陆
class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'用户名','class':'lowin-input'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'密码','class':'lowin-input'}))
    def clean_username(self):
        username = self.cleaned_data.get('username')

        filter_result = User.objects.filter(username__exact=username)
        if not filter_result:
                raise forms.ValidationError("This username does not exist. Please register first.")
        return username

    # Use clean methods to define custom validation rules
    """
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("This email does not exist.")
            else:
                filter_result = User.objects.filter(username__exact=username)
                if not filter_result:
                    raise forms.ValidationError("This username does not exist. Please register first.")
        reuturn username
    """