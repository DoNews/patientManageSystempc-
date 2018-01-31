#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from models import *
from common import *
import functools, random
import requests
import datetime
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q

#客服的患者预约工单
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
                    'serial':order.serial,#编号
                    'name':order.name, #患者姓名
                    'wanthospital':order.wanthospital.name,#医院名称
                    'wantTime':order.wantTime.strftime('%Y-%m-%d  %H:%M'),#预约时间
                    'createtime': order.createtime.strftime('%Y-%m-%d  %H:%M'),  # 提交时间
                    'status':order.get_status_display(),#患者状态
                    'is_party':order.is_party,#是否是第三方
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
    order=Order.objects.filter(id=id).first() #患者订单
    data, record = Detail(order) #data 是患者字段 包括照片，record 是所有跟进记录
    follows = OrderDetail.objects.filter(order=order)  # 对订单的所有操作
    for follow in follows: #改变orderdetail 里的操作状态
        if follow.is_operation==True:
            pass
        else:
            follow.is_operation=True
            follow.save()
    return JsonResutResponse({'ret':0,'msg':'success','data':data,'record':record})

#搜索
def Search(request):
    keyword=request.GET.get('keyword')
    page = request.GET.get('page')
    orders=Order.objects.filter(Q(name__icontains=keyword) | Q(phone__icontains=keyword) | Q(wanthospital__name__icontains=keyword)).order_by('-createtime')
    result, contacts = Paging(orders, page)
    lister=[]
    if orders:
        for order in contacts:
            data={
                'id':order.id,
                'name':order.name,
                'wanthospital':order.wanthospital.name,#医院名称
                'wantTime':order.wantTime.strftime('%Y-%m-%d  %H:%M'),#预约时间
                'status': order.get_status_display(),  # 患者状态
                'area': order.area.name,  # 所属省
                'sales': order.wanthospital.sales.name,  # 负责销售
                'createtime':order.createtime.strftime('%Y-%m-%d  %H:%M'),#提交时间
            }
            lister.append(data)
    else:
        pass
    return JsonResutResponse({'ret':0,'msg':'success','lister':lister})

#客服系统提醒
def Remind(request):
    id = request.GET.get('id')  # 客服的id
    user = ZJUser.objects.filter(id=id) #找到这个客服
    orders =Order.objects.filter(custome=user).order_by('-createtime')
    lister=RemindSystem(orders) #这是逾期的
    notes=ViewCheat(orders,user) #这里是备忘
    admins=AdminDis(orders,user) #这里是管理员分配的
    return JsonResutResponse({'ret':0,'msg':'success','lister':lister[:4],'notes':notes[:3],'admin':admins[:3]})

#查看所有逾期
def Remindall(request):
    id = request.GET.get('id')  # 客服的id
    user = ZJUser.objects.filter(id=id)  # 找到这个客服
    orders = Order.objects.filter(custome=user).order_by('-createtime')
    lister = RemindSystem(orders)
    return JsonResutResponse({'ret': 0, 'msg': 'success', 'lister': lister})

#查看所有备忘
def Cheatall(request):
    id = request.GET.get('id')  # 客服的id
    user = ZJUser.objects.filter(id=id)  # 找到这个客服
    orders = Order.objects.filter(custome=user).order_by('-createtime')
    notes = ViewCheat(orders, user)  # 这里是备忘
    return JsonResutResponse({'ret':0,'msg':'success','notes':notes})

#查看所有管理员分配
def adminsall(request):
    id = request.GET.get('id')  # 客服的id
    user = ZJUser.objects.filter(id=id)  # 找到这个客服
    orders = Order.objects.filter(custome=user).order_by('-createtime')
    admins = AdminDis(orders.user)  # 这里是管理员分配的
    return JsonResutResponse({'ret': 0, 'msg': 'success', 'admins': admins})

#客服的数据统计
def Statistics(request):
    id = request.GET.get('id')  # 客服的id
    user = ZJUser.objects.filter(id=id)  # 找到这个客服
    orders=Order.objects.filter(custome=user)#客服的全部数据
    monthorder=Order.objects.filter(createtime__month=datetime.datetime.now().month,custome=user) #本月的全部数据
