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
    path('public_job.html/del_info',views.del_job,name='del_job'),
    path('list.html/',views.list, name='list'),
    path('send_resume/',views.send_resume, name='send_resume'),
]