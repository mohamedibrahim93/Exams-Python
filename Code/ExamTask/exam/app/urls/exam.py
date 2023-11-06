from django.urls import re_path
from ..Views import exam as views


urlpatterns= [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^create$', views.create, name='create'),
    re_path(r'^generate$', views.generate, name='generate'),
    re_path(r'^addquestions/(?P<id>\d+)$', views.assign, name='addquestions'),
    re_path(r'^getquestions/(?P<id>\d+)$', views.getquestions, name='getquestions'),
    re_path(r'^getexamquestions/(?P<id>\d+)$', views.getexamquestions, name='getexamquestions'),
    re_path(r'^designexam/(?P<id>\d+)$', views.designexam, name='designexam'),
    re_path(r'^remvefromexam/(?P<id>\d+)/(?P<eid>\d+)$', views.remvefromexam, name='remvefromexam'),
    re_path(r'^addtoexam/(?P<id>\d+)/(?P<eid>\d+)$', views.addtoexam, name='addtoexam'),
    re_path(r'^printexam/(?P<id>\d+)$', views.printexam, name='printexam'),
    re_path(r'^getexams/(?P<id>\d+)$', views.getexams, name='getexams'),
    re_path(r'^edit/(?P<id>\d+)$', views.edit, name='edit'),
    re_path(r'^edit/update/(?P<id>\d+)$', views.update, name='update'),
    re_path(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),

]