#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from models import *
from common import *
import functools, random
import requests
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

#客服的患者预约工单
# @login_required(login_url="/login/")
def ServiceApoint(request):
    id=request.GET.get('id') #客服的id
    page=request.GET.get('page')
    user=ZJUser.objects.filter(id=id)
    if user : #判断是否有这个客服
        orders=Order.objects.filter(custome=user).order_by('-createtime') #该客服对应的所有工单
        result, contacts = Paging(orders, page)
        lister=[]
        if orders:
            for order in contacts:
                data={
                    'id':order.id,
                    'name':order.name, #患者姓名
                    'wanthospital':order.wanthospital.name,#医院名称
                    'wantTime':order.wantTime.strftime('%Y-%m-%d  %H:%M'),#预约时间
                    'status':order.get_status_display(),#患者状态
                    'area':order.area.name,#所属省
                    'sales':order.wanthospital.sales.name,#负责销售
                }
                lister.append(data)
        else:
            pass
        return JsonResutResponse({'ret':0,'msg':'success','lister':lister})
    else:
        return JsonResutResponse({'ret':1,'msg':'没有这个员工'})

#点击查看患者详情
def PatiDetails(request):
    id=request.GET.get('id')#患者订单的id
    order=Order.objects.filter(id=id).first()

    pass

