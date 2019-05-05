from django.urls import path

from . import views
app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('index.html/',views.index,name='index'),
    path('login.html/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('selfinfo.html/',views.self_info,name='self_info'),
    path('resumeinfo.html/<str:op>',views.resume_info,name='resume_info'),
    path('notifyinfo.html/',views.notify_info,name='notify_info'),
    path('public_job.html/',views.public_job,name='public_job'),
    path('job_detail.html/',views.job_detail,name='job_detail'),
    path('list.html/<str:ret>',views.list_job, name='list'),
    path('company.html/<str:ret>',views.list_company, name='company'),
    path('company_detail.html/',views.company_detail, name='company_detail'),
    path('send_resume/',views.send_resume, name='send_resume'),
    path('resume/',views.resume_show, name='resume_show'),
    path('eliminate/',views.eliminate_stu, name='eliminate_stu'),
    path('employ_success/',views.employ_success, name='employ_success'),
    path('del_his_resume/',views.del_his_resume, name='del_his_resume'),
    path('register_stu/',views.register_stu, name='register_stu'),
    path('register_com/',views.register_com, name='register_com'),
    path('hr_del_notify/',views.hr_del_notify, name='hr_del_notify'),

]