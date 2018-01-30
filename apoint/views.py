#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required, user_passes_test
import datetime
# Create your views here.
from models import *
def checkUser():
    pass

@login_required(login_url="/login/")
def index(request):
    # print "拿到的是什么",request.user.is_active
    #all_datas = YourModel.objects.filter(time__year=now_time.year) #查询某年的
    #all_datas = YourModel.objects.filter(time__month=now_time.month)#查询当前月份的
    thismonth=OrderDetail.objects.filter(creater=request.user).filter(createtime__month=datetime.datetime.now().month)#本月跟进工单
    thismonthfp = OrderDetail.objects.filter(creater__is_superuser=True).filter(status=OrderStatus.已安排治疗.value).filter(createtime__month=datetime.datetime.now().month) #本月分配
    thismonthrl =OrderDetail.objects.filter(createtime__month=datetime.datetime.now().month).filter(status=OrderStatus.已认领未确认)
    #todaywork = Order.objects.filter(nextcalldate)
    manag = request.user

    #identity=manag.usertype #身份(1,'客服')(2,'销售'),(3,'管理员')

    return  render(request,"index.html",{"user":manag})


def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/index")
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html', {})


    return render(request,"login.html")

