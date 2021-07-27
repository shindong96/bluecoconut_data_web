from django.conf.urls import include, url
from django.contrib import admin
from bluecoconut.views import *
from . import views

urlpatterns = [
    url(r'^$', views.post_main , name='main'),
    url(r'^map/', include('map.urls')),
    url(r'^table_view/', include('table_view.urls')),
    url(r'^accounts/login/', views.user_login, name='user_login'),
    url(r'^accounts/signup/', views.user_signup, name='user_signup'),
    url(r'^logout/', views.user_logout, name='user_logout'),
    url(r'^admin/', include(admin.site.urls)),
]
