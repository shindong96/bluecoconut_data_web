from django.conf.urls import include, url
from django.contrib import admin
from table_view.views import *
from table_view.lib import *

urlpatterns = [
    url(r'^$', TableListView.as_view() , name='table_main'),
    url(r'^detail$', TableDetailListView.as_view(), name='table_detail'),
    url(r'^detail/(?P<pk>\d+)$', TableDetailListView.as_view(), name='table_detail'),
    url(r'^download/(?P<pk>\d+)$', csv_create, name='download'),
    url(r'^cycle_download/(?P<pk>\d+)/(?P<cycle>\d+)$', cycle_csv_create, name='cycle_download'),
    url(r'^data_visual/(?P<cycle>\d+)$', map_data_print, name='map_data_print'),
]