from django.conf.urls import include, url
from django.contrib import admin
from . import views
from map.lib import csv_update
# from map.views import *

urlpatterns = [
    url(r'^$', views.map_main , name='main'),
    # url(r'^$', Map_Markup.as_view() , name='main'),
    # /argo/argo_number
    url(r'^argo_data/(?P<pk>\d+)$', views.argo_data , name='argo_data'),
    # ajax 참고 url(r'^admin/employee_info/remove/(?P<pk>\d+)$', EmployeeDeleteView.as_view(), name='employee_remove'),
    url(r'^csv_update/(?P<pk>\d+)/(?P<cycle>\d+)$', csv_update, name='csv_update'),

]