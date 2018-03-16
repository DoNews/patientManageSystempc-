#coding:utf-8
from django.conf.urls import url

from apoint.Views.view_wx import *
from apoint.Views.views import *
from apoint.Views.service_views import *

urlpatterns = [
    url(r'^scrfcode/',ScrfCode), #发送验证码
    url(r'^staff/',StaffCation),#员工认证
    url(r'^mypatien/',MyPatients),#员工对应的患者
    url(r'^patientsdetail/',PatientsDetail),#查看患者详情 ——做了简单的修改
    url(r'^lookcheat/',LookCheat),#查看所有的备忘 ---------新加
    url(r'^thememo/',TheMemo),#员工提交备忘录
    url(r'^cilckmake/',CilckMake),#患者点击去预约
    url(r'^ordersubmit/',PhoneOrder),#患者提交预约
    url(r'^orderdetailser/',OrderDeta),#患者详情
    url(r'^upload/',uploader),#图片上传
    url(r'^province/',Province),#所有省
    url(r'^hospital/',Hospitaltable),#所有医院
    url(r'^checkphone',checkphone),#员工认证
    url(r'^patsearch/',PatSearch),#患者搜索


    #客服
    url(r'^service/',ServiceApoint), #客服的患者预约工单
    url(r'^patidetails/',PatiDetails),#客服点击查看患者详情
    url(r'^search/',Search),#搜索
    url(r'^remind/',Remind),#客服系统提醒
    url(r'^remindall/',Remindall),#查看所有逾期
    url(r'^cheatall/',Cheatall),#查看所有备忘
    url(r'^adminsall/',Adminsall),#查看所有管理员分配
    url(r'^statistics/',Statistics),##客服的数据统计
    url(r'^thirdparty/',ThirdParty),#第三方导入数据的接口

    #管理员
    url(r'^stafman/',StafManag),##管理员的销售和客服管理
    url(r'^staffall/',StaffAll),#查看所有销售
    url(r'^AccountAll',AccountAll),
    url(r'^staffeditor/',StaffEditor),#查看销售详情
    url(r'^addstaff/',AddStaff),#添加销售和修改销售
    url(r'^queryhosp/',QueryHosp),##查询医院(一省对应一个医院列表)
    url(r'^staffdelete/',StaffDelete),#删除销售或者客服
    url(r'^orderall/',OrderAll),#查看所有患者
    url(r'^allhospit/',Allhospit),#查看所有医院
    url(r'^allnoservit/',AllNoservit),#查看第三方全部
    url(r'^ordermerge/',OrderMerge),#患者归并和拆分
    url(r'^redisbution/',RedisBution),#患者去管理重新分配客服
    url(r'^hospitment/',HospitMent),#查看医院详情
    url(r'^addhosp/',AddHosp),#医院的添加和修改
    url(r'^adminstatic/',adminStatic),#管理员的数据统计
    url(r'^updateSalesHosp', updateSalesHosp),
    url(r'^AccountSet',AccountSet),#客服账号设置
    url(r'^hairsms',SMSnote),#发验证码
]