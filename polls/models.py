from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from . import common

#公司信息
class Company(models.Model):
    #名字
    name               = models.CharField(max_length=100,verbose_name="公司",blank=False,default='')
    #公司规模
    scale              = models.CharField(max_length=2,choices=common.sca_choice,default='1',verbose_name='公司规模')
    #融资阶段
    financing          = models.CharField(max_length=2,choices=common.fin_choice,default='1',verbose_name='融资阶段')
    #行业类型
    industry_type      = models.CharField(max_length=2,choices=common.ind_choice,default='1',verbose_name='行业类型')
    #公司简介
    desc               = models.TextField(max_length=2000,verbose_name='公司简介')
    #公司地点
    city               = models.CharField(max_length=2,choices=common.city_choice,default='0',verbose_name='公司总部')
    #热度值 = 所有岗位热度值之和
    hot_val            = models.IntegerField(verbose_name='热度值',default=0)
    def __str__(self):
        return self.name

#学生用户 的信息
class UserProfile(models.Model):
    user               = models.OneToOneField(User, on_delete=models.CASCADE, related_name='StuProfile')
    name               = models.CharField(max_length=50,verbose_name="姓名",blank=False,default='')
    gender             = models.CharField(max_length=2, choices=(('1','男'),('2','女'),('3','未填写')),verbose_name="性别",blank=True,default='3')
    phone              = models.CharField(max_length=200,verbose_name="联系方式",blank=True,default='')
    
    def __str__(self):
        return self.user.username

#人事专业HR 的信息
class HRProfile(models.Model):
    user               = models.OneToOneField(User, on_delete=models.CASCADE, related_name='HRProfile')
    name               = models.CharField(max_length=50,verbose_name="姓名",blank=False,default='')
    gender             = models.CharField(max_length=2, choices=(('1','男'),('2','女'),('3','未填写')),verbose_name="性别",blank=True,default='3')
    phone              = models.CharField(max_length=200,verbose_name="联系方式",blank=True,default='')
    company            = models.ForeignKey(Company,on_delete=models.CASCADE,null=True)
    identify           = models.CharField(max_length=2, choices=(('1','已认证'),('2','未认证')),verbose_name="认证",blank=False,default='2')
    def __str__(self):
        return self.user.username

#教育经历
class Edu_experience(models.Model):
    edu_choice=(
        ('1','专科'),
        ('2','本科'),
        ('3','硕士'),
        ('4','博士'),
    )
    #时间段
    start_date         = models.DateField()
    end_date           = models.DateField()
    #学校
    gra_school         = models.CharField(max_length=150)
    #学历
    edu                = models.CharField(max_length=10,choices=edu_choice,default='1')
    #专业
    profession         = models.CharField(max_length=50,default='')
    owner              = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=False)

    def __str__(self):
        return self.profession

#项目经验
class Pro_experience(models.Model):
    #项目时间
    start_date         = models.DateField()
    end_date           = models.DateField()
    #项目角色
    job_role           = models.CharField(max_length=50)
    #项目名称
    job_name           = models.CharField(max_length=100)
    #项目描述
    job_desc           = models.TextField(max_length=2000)

    owner              = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=False)

    def __str__(self):
        return self.job_name + ":" + self.job_role


#工作经历
class Job_experience(models.Model):
    #在职时间
    start_date         = models.DateField()
    end_date           = models.DateField()
    #公司名称
    company_name       = models.CharField(max_length=50,default='')
    #工作职位
    job_role           = models.CharField(max_length=50,default='')
    #工作描述
    job_desc           = models.TextField(max_length=2000,default='')
    #所属行业
    industry           = models.CharField(max_length=50,default='')            

    owner              = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=False)

    def __str__(self):
        return self.company_name + "-" + self.job_role

#岗位信息
class Job_position(models.Model):
    #岗位名字
    name               = models.CharField(max_length=30,verbose_name='岗位',default='')
    #工作描述
    job_desc           = models.TextField(max_length=2000,verbose_name='岗位描述')
    #就业城市
    city               = models.CharField(max_length=2,choices=common.city_choice,default='0',verbose_name='就业城市')
    #学历要求
    edu_req            = models.CharField(max_length=2,choices=common.edu_choice,default='5',verbose_name='学历要求')
    #工作经验要求
    exp_req            = models.CharField(max_length=2,choices=common.exp_choice,default='1',verbose_name='工作经验')
    #发布时间
    pub_date           = models.DateField(auto_now_add=True,verbose_name='发布时间')
    #发布者
    publisher          = models.ForeignKey(HRProfile,on_delete=models.CASCADE,default='',verbose_name='发布者')
    #薪资
    salary1            = models.IntegerField(verbose_name='薪资范围1',default=0)
    salary2            = models.IntegerField(verbose_name='薪资范围2',default=0)
    #热度值
    hot_val            = models.IntegerField(verbose_name='热度值',default=0)
    #人数需求
    need               = models.IntegerField(verbose_name='人数需求',default=0)
    #投递简历人数
    reg_num            = models.IntegerField(verbose_name='投递人数',default=0)
    def __str__(self):
        return self.name+" " + self.publisher.company.name + " 需求: " + str(self.need) + "人"


#简历投递情况
class SendResume(models.Model):
    #学生
    stu                = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=False,verbose_name="学生")
    #岗位
    sta                = models.ForeignKey(Job_position,on_delete=models.CASCADE,null=False,verbose_name="岗位")
    #投递时间
    time               = models.DateField(auto_now_add=True,verbose_name='发布时间')
    #录用状况
    is_employ          = models.CharField(max_length=2,choices=(('1','录取'),('0','待考验')),default='0',verbose_name='录取情况')
    #是否显示在前端页面
    show               = models.CharField(max_length=2,choices=(('1','显示'),('0','隐藏')),default='1',verbose_name='显示在页面')
    #消息中心显示
    show_notify        = models.CharField(max_length=2,choices=(('1','显示'),('0','隐藏')),default='1',verbose_name='显示在消息中心')
    def __str__(self):
        return str(self.time) + ":" + self.stu.name + " 投递了 " + self.sta.name + " 岗位"

#评论,一个公司有多条评论
class Comment(models.Model):
    #评论对象
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=False,verbose_name="被评论公司")
    #评论人，只能是学生
    stu     = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=False,verbose_name="评论人")
    #评论内容
    com     = models.TextField(max_length=2000,verbose_name='评论内容')
    #评论时间
    created = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    def __str__(self):
        return str(self.created)+"  "+str(self.stu.name)+ "发表了评论"