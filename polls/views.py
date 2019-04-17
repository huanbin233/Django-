from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.contrib import messages
from .models import UserProfile,Edu_experience,Pro_experience,Job_experience,Job_position,HRProfile,SendResume,Company
from django.contrib.auth.models import User
from .forms import ComRegisterForm,StuRegisterForm,LoginForm,EduForm,ProForm,JobForm,StationForm,Company_filter,Job_filter
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.forms.utils import ErrorDict

from django_tables2 import RequestConfig
from .tables import PersonTable
#主页
def index(request):
    tengxun = Company.objects.get(name="腾讯")
    baidu = Company.objects.get(name="百度")
    alibaba = Company.objects.get(name="阿里巴巴")
    wangyi = Company.objects.get(name="网易")
    jingdong = Company.objects.get(name="京东")
    sougou = Company.objects.get(name="搜狗")
    meituan = Company.objects.get(name="美团点评")
    xiaomi  = Company.objects.get(name="小米")
    xinlang = Company.objects.get(name="新浪")
    huawei = Company.objects.get(name="华为")
    return render(request, 'polls/index.html', locals())

#登陆
def login(request):
    login_Form = LoginForm()
    if request.method == 'POST':
        #登陆
        login_Form = LoginForm(request.POST)
        if login_Form.is_valid():
            username = login_Form.cleaned_data['username']
            password = login_Form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('/polls/index.html',locals())
        else:
            print(login_Form.non_field_errors())
    return render(request,'polls/signin.html',locals())

#学生注册
def register_stu(request):
    is_stu = 1
    Register_Form = StuRegisterForm()
    if request.method == 'POST':
        Register_Form = StuRegisterForm(request.POST)
        if Register_Form.is_valid():
            username = Register_Form.cleaned_data['username']
            password = Register_Form.cleaned_data['password']
            comfirm_passwd = Register_Form.cleaned_data['comfirm_passwd']
            email = Register_Form.cleaned_data['email']

            user = User.objects.create_user(username=username, password=password,email=email)
            user_profile = UserProfile.objects.create(user = user)
            return HttpResponseRedirect('/polls/login.html')
        else:
            print(Register_Form.non_field_errors())
    return render(request,'polls/signup.html',locals()) 

#企业注册
def register_com(request):
    is_stu = 0
    Register_Form = ComRegisterForm()
    if request.method == 'POST':
        Register_Form = ComRegisterForm(request.POST)
        if Register_Form.is_valid():
            username = Register_Form.cleaned_data['username']
            password = Register_Form.cleaned_data['password']
            email = Register_Form.cleaned_data['email']
            comfirm_passwd = Register_Form.cleaned_data['comfirm_passwd']

            user = User.objects.create_user(username=username, password=password, email=email)
            hr_profile = HRProfile.objects.create(user = user)
            return HttpResponseRedirect('/polls/login.html')
        else:
            print(Register_Form.non_field_errors())
    return render(request,'polls/signup.html',locals()) 
    
#退出登录
def logout(request):
    auth.logout(request)
    return redirect('/polls/index.html')

#个人中心
#个人信息
@login_required
def self_info(request):
    is_stu = True
    try:
        loginuser = UserProfile.objects.get(user__exact=request.user)
    except:
        loginuser = HRProfile.objects.get(user__exact=request.user)
        is_stu = False
    if request.method == 'POST':
        #获取当前的用户
        #在这个基础上修改
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']
        user = User.objects.get(username=loginuser[0].user.username)
        if is_stu == False:
            profile = HRProfile.objects.get(user=user)
        else:
            profile = UserProfile.objects.get(user=user)
        
        user.email = email

        profile.phone = phone
        profile.name = name

        if gender=='male':
            profile.gender = '1'
        elif gender=='female':
            profile.gender = '2'

        user.save()
        profile.save()
        return HttpResponseRedirect('/polls/selfinfo.html')
    return render(request, 'polls/selfinfo.html', locals())

#个人简历，包括工作经历,教育经历,项目经历等等
@login_required
def resume_info(request,op):
    if op == 'del_edu':
        did = request.GET.get('did')
        Edu_experience.objects.filter(id=did).delete()
        return HttpResponseRedirect('/polls/resumeinfo.html/check')
    elif op == 'del_pro':
        did = request.GET.get('did')
        Pro_experience.objects.filter(id=did).delete()
        return HttpResponseRedirect('/polls/resumeinfo.html/check')
    elif op == 'del_job':
        did = request.GET.get('did')
        Job_experience.objects.filter(id=did).delete()
        return HttpResponseRedirect('/polls/resumeinfo.html/check')        

    loginuser = UserProfile.objects.get(user=request.user)
    edu_exp = Edu_experience.objects.filter(owner=loginuser)
    pro_exp = Pro_experience.objects.filter(owner=loginuser)
    job_exp = Job_experience.objects.filter(owner=loginuser)
    edu_form = EduForm()
    pro_form = ProForm()
    job_form = JobForm()

    if request.method == 'POST':
        edu_Form = EduForm(request.POST)
        if edu_Form.is_valid():
            school = edu_Form.cleaned_data['school']
            pro = edu_Form.cleaned_data['pro']
            start_date = edu_Form.cleaned_data['start_date']
            end_date = edu_Form.cleaned_data['end_date']
            edu = edu_Form.cleaned_data['edu']

            exp = Edu_experience.objects.create(gra_school=school,profession=pro,start_date=start_date,end_date=end_date,edu=edu,owner=loginuser)
            exp.save()
            return HttpResponseRedirect('/polls/resumeinfo.html/check')

        pro_Form = ProForm(request.POST)
        if pro_Form.is_valid():
            job_name = pro_Form.cleaned_data['job_name']
            job_role = pro_Form.cleaned_data['job_role']
            job_desc = pro_Form.cleaned_data['job_desc']
            start_date = pro_Form.cleaned_data['start_date']
            end_date = pro_Form.cleaned_data['end_date']

            exp = Pro_experience.objects.create(job_name=job_name,job_desc=job_desc,job_role=job_role,start_date=start_date,end_date=end_date,owner=loginuser)
            exp.save()
            return HttpResponseRedirect('/polls/resumeinfo.html/check')

        job_Form = JobForm(request.POST)
        if job_Form.is_valid():
            company_name = job_Form.cleaned_data['company_name']
            job_role = job_Form.cleaned_data['job_role']
            job_desc = job_Form.cleaned_data['job_desc']
            start_date = job_Form.cleaned_data['start_date']
            end_date = job_Form.cleaned_data['end_date']
            industry = job_Form.cleaned_data['industry']

            exp = Job_experience.objects.create(company_name=company_name,job_desc=job_desc,job_role=job_role,start_date=start_date,end_date=end_date,industry=industry,owner=loginuser)
            exp.save()
            return HttpResponseRedirect('/polls/resumeinfo.html/check')

    return render(request, 'polls/resumeinfo.html', locals())

#通知消息
@login_required
def notify_info(request):
    is_stu = True
    try:
        loginuser = UserProfile.objects.get(user__exact=request.user)
    except:
        loginuser = HRProfile.objects.get(user__exact=request.user)
        is_stu = False
    table = PersonTable(UserProfile.objects.all())
    RequestConfig(request, paginate={'per_page': 1}).configure(table)
    return render(request, 'polls/notifyinfo.html', locals())

#已发布招聘
@login_required
def public_job(request):
    loginuser = HRProfile.objects.get(user__exact=request.user)
    pub_job = Job_position.objects.filter(publisher=loginuser)
    stationForm = StationForm()

    if request.method == 'POST':
        station_Form = StationForm(request.POST)
        if station_Form.is_valid():
            name = station_Form.cleaned_data['name']
            edu_req = station_Form.cleaned_data['edu_req']
            need = station_Form.cleaned_data['need']
            job_desc = station_Form.cleaned_data['job_desc']
            city     = station_Form.cleaned_data['city']
            salary1= station_Form.cleaned_data['salary1']
            salary2= station_Form.cleaned_data['salary2']
            station = Job_position.objects.create(salary2=salary2,salary1=salary1,name=name,
                edu_req=edu_req,need=need,publisher=loginuser,job_desc=job_desc,city=city)
            station.save()

            return HttpResponseRedirect('/polls/public_job.html')
        
    return render(request, 'polls/public_job.html', locals())

@login_required
def del_job(request):
    id = request.GET.get('id')
    Job_position.objects.filter(id=id).delete()
    return HttpResponseRedirect('/polls/public_job.html') 

#过滤岗位信息
def job_filter_all(ret,job_list_all):
    filter = ret.split("_")
    job_filter = Job_filter()
    job_filter.set_city(filter[0])
    job_filter.set_salary_req(filter[1])

    salary_min_vec = [0,0,3,5,10,15,20,25,30]
    salary_max_vec = [0,3,5,10,15,20,25,20,1000000]
    #城市筛选信息非 不限
    if filter[0] != '0':
        job_list_all = job_list_all.filter(city=filter[0])
    #薪资筛选信息非 不限
    if filter[1] != '0':
        salary_min = salary_min_vec[int(filter[1])]
        salary_max = salary_max_vec[int(filter[1])]
        job_list_all = job_list_all.filter(salary1__gte=salary_min)
        job_list_all = job_list_all.filter(salary1__lte=salary_max)
    
    return job_filter,job_list_all

def list_job(request,ret):
    if request.method == 'POST':
        city_filter = request.POST.get('city_filter')
        salary_filter = request.POST.get('salary_filter')
        result = [str(city_filter), str(salary_filter)]
        return HttpResponseRedirect('/polls/list.html/' + "_".join(result))
    
    job_list_all = Job_position.objects.exclude(need__lte=0)
    
    #根据过滤条件,过滤掉信息
    job_filter,job_list_all = job_filter_all(ret,job_list_all)

    #book_list_all 是要被分页的对象，第二个参数，是每页显示的条数
    p = Paginator(job_list_all,7)# p就是每页的对象，
    p.count  #数据总数
    p.num_pages  #总页数
    p.page_range#[1,2,3,4,5],得到页码，动态生成，

    page_num = request.GET.get("page")#以get的方法从url地址中获取
    try:
        job_list = p.page(page_num)#括号里的是页数，显示指定页码的数据，动态显示数据，所以不能写死了
    except PageNotAnInteger:#如果输入页码错误，就显示第一页
        job_list = p.page(1)
    except EmptyPage:#如果超过了页码范围，就把最后的页码显示出来，
        job_list = p.page(p.num_pages)
    
    hot_list = job_list_all.order_by('-hot_val')[:10]
    new_list = job_list_all.order_by('-pub_date')[:10]
    return render(request, 'polls/list.html', locals())

#公司列表,第二个参数是筛选结果a_b_c分别对应每个select下拉框的筛选值
def list_company(request, ret):
    if request.method == 'POST':
        type_filter = request.POST.get('type_filter')
        fin_filter = request.POST.get('fin_filter')
        sca_filter = request.POST.get('sca_filter')
        result = [str(type_filter), str(fin_filter), str(sca_filter)]
        return HttpResponseRedirect('/polls/company.html/' + "_".join(result))
    
    filter = ret.split("_")
    com_filter = Company_filter()
    com_filter.set_type(filter[0])
    com_filter.set_fin(filter[1])
    com_filter.set_scale(filter[2])
    company_lis_all = Company.objects.all()
    if filter[0] != '0':
        company_lis_all = company_lis_all.filter(industry_type=filter[0])
    if filter[1] != '0':
        company_lis_all = company_lis_all.filter(financing=filter[1])
    if filter[2] != '0':
        company_lis_all = company_lis_all.filter(scale=filter[2])
    p = Paginator(company_lis_all,12)# p就是每页的对象，
    p.count  #数据总数
    p.num_pages  #总页数
    p.page_range#[1,2,3,4,5],得到页码，动态生成，

    page_num = request.GET.get("page")#以get的方法从url地址中获取
    try:
        company_list = p.page(page_num)#括号里的是页数，显示指定页码的数据，动态显示数据，所以不能写死了
    except PageNotAnInteger:#如果输入页码错误，就显示第一页
        company_list = p.page(1)
    except EmptyPage:#如果超过了页码范围，就把最后的页码显示出来，
        company_list = p.page(p.num_pages)
    
    return render(request, 'polls/company.html', locals())

#简历投递
@login_required
def send_resume(request):
    sid = request.GET.get("sid")
    cur_page = request.GET.get("cur_page")
    try:
        position = Job_position.objects.get(id=sid)
        loginuser = UserProfile.objects.get(user__exact=request.user)
        is_exists = SendResume.objects.filter(stu = loginuser, sta = position)
        if is_exists.count() != 0:
            messages.error(request,"请不要重复投递！")
        else:
            contact = SendResume.objects.create(stu = loginuser, sta = position)
            contact.save()
            #投递简历，岗位热度值要+10
            position.hot_val += 10
            #统计投递人数
            position.reg_num += 1
            position.save()
            messages.success(request,"简历投递成功，请耐心等候通知！")
    except:
        messages.error(request,"您当前的身份不能进行简历投递！") 
    #在职位详情页面投递简历
    if cur_page == '2':
        return HttpResponseRedirect('/polls/job_detail.html?id=%s' % (sid)) 
    #在公司详情页面投递简历
    elif cur_page == '3':
        return HttpResponseRedirect('/polls/company_detail.html?id=%s' 
                                        % (position.publisher.company.id))         
    #在职位列表页面投递简历
    else:
        page_num = request.GET.get("page")
        return HttpResponseRedirect('/polls/list.html?page=%s' % (page_num)) 

#公司详情信息
def company_detail(request):
    com_id = request.GET.get("id")
    com = Company.objects.get(id=com_id)
    active_panel = 1
    job_list_all = filter_job_with_company(com)
    #book_list_all 是要被分页的对象，第二个参数，是每页显示的条数
    p = Paginator(job_list_all,5)# p就是每页的对象，
    p.count  #数据总数
    p.num_pages  #总页数
    p.page_range#[1,2,3,4,5],得到页码，动态生成，

    page_num = request.GET.get("page")#以get的方法从url地址中获取
    try:
        job_list = p.page(page_num)#括号里的是页数，显示指定页码的数据，动态显示数据，所以不能写死了
        active_panel = 3
    except PageNotAnInteger:#如果输入页码错误，就显示第一页
        job_list = p.page(1)
    except EmptyPage:#如果超过了页码范围，就把最后的页码显示出来，
        job_list = p.page(p.num_pages)
    
    if com:
        return render(request, 'polls/company_detail.html', locals())

def job_detail(request):
    job_id = request.GET.get("id")
    job = Job_position.objects.get(id=job_id)
    stu_list_all = SendResume.objects.filter(sta=job,show='1')
    active_panel = 1
    p = Paginator(stu_list_all,5)# p就是每页的对象，
    p.count  #数据总数
    p.num_pages  #总页数
    p.page_range#[1,2,3,4,5],得到页码，动态生成，

    page_num = request.GET.get("page")#以get的方法从url地址中获取
    try:
        stu_list = p.page(page_num)#括号里的是页数，显示指定页码的数据，动态显示数据，所以不能写死了
        active_panel = 3
    except PageNotAnInteger:#如果输入页码错误，就显示第一页
        stu_list = p.page(1)
        page_num = 1
    except EmptyPage:#如果超过了页码范围，就把最后的页码显示出来，
        stu_list = p.page(p.num_pages)
        page_num = p.num_pages
    return render(request, 'polls/job_detail.html', locals())

#过滤出指定公司的岗位
def filter_job_with_company(com):
    job_list_all = Job_position.objects.exclude(need__lte=0)
    job_list = []
    for job in job_list_all:
        puber = job.publisher
        if puber.company == com:
            job_list.append(job)
    return job_list

#简历展示页面
def resume_show(request):
    #获得学生id
    stu_id = request.GET.get("id")
    #检验学生id数据是否有效
    if stu_id == '':
        return render(request, 'polls/404_not_found.html', locals())
    try:
        #获取个人信息
        self_info = UserProfile.objects.get(id = stu_id)
        #获取工作经历
        job_exp = Job_experience.objects.filter(owner=self_info)
        #获取项目经历
        pro_exp = Pro_experience.objects.filter(owner=self_info)
        #获取教育经历
        edu_exp = Edu_experience.objects.filter(owner=self_info)
        return render(request, 'polls/resume.html', locals())
    except:
        return render(request, 'polls/404_not_found.html', locals())

#淘汰学生
def eliminate_stu(request):
    resume_id = request.GET.get("id")
    page = request.GET.get("page")
    try:
        resumeinfo = SendResume.objects.get(id=resume_id)
        job_id = resumeinfo.sta.id;
        resumeinfo.delete()
        if page=='':
            page=1
        return HttpResponseRedirect('/polls/job_detail.html?id={0}&page={1}'.format(job_id,page))
    except:
        return render(request, 'polls/404_not_found.html', locals())

#录用
def employ_success(request):
    resume_id = request.GET.get("id")
    page = request.GET.get("page")
    try:
        resumeinfo = SendResume.objects.get(id=resume_id)
        job_id = resumeinfo.sta.id;
        resumeinfo.sta.need -= 1
        resumeinfo.is_employ = '1'
        resumeinfo.sta.save()
        resumeinfo.save()
        if page=='':
            page=1
        return HttpResponseRedirect('/polls/job_detail.html?id={0}&page={1}'.format(job_id,page))
    except:
        return render(request, 'polls/404_not_found.html', locals())

def del_his_resume(request):
    resume_id = request.GET.get("id")
    page = request.GET.get("page")
    try:
        resumeinfo = SendResume.objects.get(id=resume_id)
        job_id = resumeinfo.sta.id;
        resumeinfo.show = '0'
        resumeinfo.save()
        if page=='':
            page=1
        return HttpResponseRedirect('/polls/job_detail.html?id={0}&page={1}'.format(job_id,page))
    except:
        return render(request, 'polls/404_not_found.html', locals())