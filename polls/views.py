from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.contrib import messages
from .models import UserProfile,Edu_experience,Pro_experience,Job_experience,Job_position,HRProfile,SendResume
from django.contrib.auth.models import User
from .forms import ComRegisterForm,StuRegisterForm,LoginForm,EduForm,ProForm,JobForm,StationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
#主页
def index(request):
    return render(request, 'polls/index.html', {'request':request})

#登录or注册
def login(request):
    context={}
    login_Form = LoginForm()
    stuRegister_Form = StuRegisterForm()
    comRegister_Form = ComRegisterForm()

    context['LoginForm'] = login_Form
    context['stuRegisterForm'] = stuRegister_Form
    context['comRegisterForm'] = comRegister_Form
    if request.method == 'POST':
        #登陆
        login_Form = LoginForm(request.POST)
        if login_Form.is_valid():
            username = login_Form.cleaned_data['username']
            password = login_Form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('/polls/index.html',{'request':request})
            else:
                return render(request, 'polls/login.html', context)
        #企业注册
        comRegister_Form = ComRegisterForm(request.POST)
        if comRegister_Form.is_valid():
            company = comRegister_Form.cleaned_data['company']
            username = comRegister_Form.cleaned_data['username']
            password = comRegister_Form.cleaned_data['password']
            email = comRegister_Form.cleaned_data['email']
            phone = comRegister_Form.cleaned_data['phone']

            user = User.objects.create_user(username=username, password=password, email=email)
            hr_profile = HRProfile(user=user, phone=phone,company=company)

            hr_profile.save()
        #学生注册
        stuRegister_Form = StuRegisterForm(request.POST)
        if stuRegister_Form.is_valid():
            username = stuRegister_Form.cleaned_data['username']
            password = stuRegister_Form.cleaned_data['password']
            email = stuRegister_Form.cleaned_data['email']
            phone = stuRegister_Form.cleaned_data['phone']

            user = User.objects.create_user(username=username, password=password,email=email)
            user_profile = UserProfile(user = user,phone=phone)

            user_profile.save()


            #messages.add_message(request, messages.INFO, "注册成功，跳转到登录界面")                                                
    return render(request,'polls/login.html',context)

#退出登录
def logout(request):
    auth.logout(request)
    return redirect('/polls/index.html')

#个人中心
#个人信息
@login_required
def self_info(request):
    is_stu = True
    loginuser = UserProfile.objects.filter(user__exact=request.user)
    if loginuser.count() == 0:
        loginuser = HRProfile.objects.filter(user__exact=request.user)
        is_stu = False

    context={'request':request,'loginuser':loginuser[0],'is_stu':is_stu}
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
    return render(request, 'polls/selfinfo.html', context)

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

    loginuser = UserProfile.objects.filter(user__exact=request.user)
    context={'request':request,'loginuser':loginuser[0]}

    edu_exp = Edu_experience.objects.filter(owner=loginuser[0])
    context['edu_exp'] = edu_exp

    pro_exp = Pro_experience.objects.filter(owner=loginuser[0])
    context['pro_exp'] = pro_exp

    job_exp = Job_experience.objects.filter(owner=loginuser[0])
    context['job_exp'] = job_exp

    edu_form = EduForm()
    context['edu_form'] = edu_form  

    pro_form = ProForm()
    context['pro_form'] = pro_form

    job_form = JobForm()
    context['job_form'] = job_form

    if request.method == 'POST':
        edu_Form = EduForm(request.POST)
        if edu_Form.is_valid():
            school = edu_Form.cleaned_data['school']
            pro = edu_Form.cleaned_data['pro']
            start_date = edu_Form.cleaned_data['start_date']
            end_date = edu_Form.cleaned_data['end_date']
            edu = edu_Form.cleaned_data['edu']

            exp = Edu_experience.objects.create(gra_school=school,profession=pro,start_date=start_date,end_date=end_date,edu=edu,owner=loginuser[0])
            exp.save()
            return HttpResponseRedirect('/polls/resumeinfo.html/check')

        pro_Form = ProForm(request.POST)
        if pro_Form.is_valid():
            job_name = pro_Form.cleaned_data['job_name']
            job_role = pro_Form.cleaned_data['job_role']
            job_desc = pro_Form.cleaned_data['job_desc']
            start_date = pro_Form.cleaned_data['start_date']
            end_date = pro_Form.cleaned_data['end_date']

            exp = Pro_experience.objects.create(job_name=job_name,job_desc=job_desc,job_role=job_role,start_date=start_date,end_date=end_date,owner=loginuser[0])
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

            exp = Job_experience.objects.create(company_name=company_name,job_desc=job_desc,job_role=job_role,start_date=start_date,end_date=end_date,industry=industry,owner=loginuser[0])
            exp.save()
            return HttpResponseRedirect('/polls/resumeinfo.html/check')

    return render(request, 'polls/resumeinfo.html', context)

#通知消息
@login_required
def notify_info(request):
    is_stu = True
    loginuser = UserProfile.objects.filter(user__exact=request.user)
    if loginuser.count() == 0:
        loginuser = HRProfile.objects.filter(user__exact=request.user)
        is_stu = False
    context={'request':request,'loginuser':loginuser[0],'is_stu':is_stu}

    return render(request, 'polls/notifyinfo.html', context)

#已发布招聘
@login_required
def public_job(request):
    loginuser = HRProfile.objects.filter(user__exact=request.user)
    context={'request':request,'loginuser':loginuser[0]}

    pub_job = Job_position.objects.filter(publisher=loginuser[0])
    context['pub_job'] = pub_job

    stationForm = StationForm()
    context['stationForm'] = stationForm  

    if request.method == 'POST':
        station_Form = StationForm(request.POST)
        if station_Form.is_valid():
            name = station_Form.cleaned_data['name']
            edu_req = station_Form.cleaned_data['edu_req']
            exp_req = station_Form.cleaned_data['exp_req']
            job_desc = station_Form.cleaned_data['job_desc']
            city     = station_Form.cleaned_data['city']
            salary = station_Form.cleaned_data['salary']
            station = Job_position.objects.create(salary=salary,name=name,edu_req=edu_req,exp_req=exp_req,publisher=loginuser[0],job_desc=job_desc,city=city)
            station.save()

            return HttpResponseRedirect('/polls/public_job.html')
        
    return render(request, 'polls/public_job.html', context)

@login_required
def del_job(request):
    did = request.GET.get('did')
    Job_position.objects.filter(id=did).delete()
    return HttpResponseRedirect('/polls/public_job.html') 
    
def list(request):
    job_list_all = Job_position.objects.all()
    #book_list_all 是要被分页的对象，第二个参数，是每页显示的条数
    p = Paginator(job_list_all,8)# p就是每页的对象，
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
    return render(request, 'polls/list.html', locals())

@login_required
def send_resume(request):
    loginuser = UserProfile.objects.filter(user__exact=request.user)
    sid = request.GET.get("sid")
    position = Job_position.objects.filter(id=sid)
    if loginuser.count() == 0 or position.count() == 0:
        messages.error(request,"失败，请确保您已经以学生账号登录！")
    else:
        is_exists = SendResume.objects.filter(stu = loginuser[0], sta = position[0])
        if is_exists.count() != 0:
            messages.error(request,"失败，请不要重复投递！")
        else:
            contact = SendResume.objects.create(stu = loginuser[0], sta = position[0])
            contact.save()
            messages.success(request,"投递成功！")
    return HttpResponseRedirect('/polls/list.html') 