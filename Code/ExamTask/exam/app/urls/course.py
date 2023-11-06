from django.urls import re_path
from ..Views import course as views


urlpatterns= [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^create$', views.create, name='create'),
    re_path(r'^edit/(?P<id>\d+)$', views.edit, name='edit'),
    re_path(r'^edit/update/(?P<id>\d+)$', views.update, name='update'),
    re_path(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    re_path(r'^ajax/validate_coursename/$', views.validate_coursename, name='validate_coursename'),

]