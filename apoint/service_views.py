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
                    'name':order.name #患者姓名

                }

