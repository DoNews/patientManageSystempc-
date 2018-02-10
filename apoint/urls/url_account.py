#coding: utf8
from apoint.Views.view_admin import *
from apoint.Views.view_user import *
from apoint.Views.view_user import *
from apoint.Views.views import *
from django.conf.urls import url
urlpatterns = [
    url(r'^$', index),
    url(r'^index$', index),
    url(r'^staffaddnew', staffaddnew),
    url(r'^renling$',renling),
    url(r'^createUser$',createUser),
    url(r'^renlingAction$',renlingAction),
    url(r'pations$',pations),
    url(r'^pationsview',pationsview),#客服患者数据
    url(r'^remind',remind),#全部提醒页面
    url(r'^account',account),
    url(r'^addpation',addpation),
    url(r'^chart$',chart),
    url(r'^upload',uploader),
    url(r'^orderdetail$',orderdetail),
    url(r'^ordersubmit',OrderSubmit),
    url(r'^orderupdate',OrderUpdte),

    url(r'^overdue', overdue),
    url(r'^salercommit',salercommit),
    url(r'^adminfenpei', adminfenpei),

    url(r'^staffaddnew', staffaddnew),

    url(r'^todaywork',todaywork),
    url(r'^yuqi$',yuqi)
        ]