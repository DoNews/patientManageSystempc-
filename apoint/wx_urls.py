#coding:utf-8
from django.conf.urls import url
from wx_views import *
urlpatterns = [
    url(r'^scrfcode/',ScrfCode), #发送验证码
    url(r'^staff/',StaffCation),#员工认证
    url(r'^mypatien/',MyPatients),#员工对应的患者
    url(r'^patientsdetail/',PatientsDetail),#查看患者详情
    url(r'^thememo/',TheMemo),#员工提交备忘录
    url(r'^cilckmake/',CilckMake),#患者点击去预约
    url(r'^ordersubmit/',OrderSubmit),#患者提交预约 可和pc端的共用
    url(r'^upload/',uploader),#图片上传
    url(r'^province/',Province),#所有省 可共用
    url(r'^hospital/',Hospitaltable),#所有医院 可共用

    #客服

]