#coding: utf8
"""Apointment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from apoint.views import *
from apoint.adminviews import *
import xadmin
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^index$',index),
    url(r'^login',userlogin),
    url(r'^api/pc/',include('apoint.urls')),#PC端接口
    url(r'^api/apoint/',include('apoint.wx_urls')),#微信调用接口
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'login.html'}),
    url(r'^staff$',staff),
    url(r'^renling$',renling),
]
