#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required, user_passes_test
from datetime import datetime, timedelta
# Create your views here.
from models import *
def checkUser():
    pass

@login_required(login_url="/login/")
def index(request):
    # print "拿到的是什么",request.user.is_active
    #all_datas = YourModel.objects.filter(time__year=now_time.year) #查询某年的
    #all_datas = YourModel.objects.filter(time__month=now_time.month)#查询当前月份的
    user=ZJUser.objects.get(user=request.user)
    print "user:",request.user
    now =datetime.now()
    yestoday = now- timedelta(days=1)
    thismonth=OrderDetail.objects.filter(creater=user).filter(createtime__month=now.month).count()#本月跟进工单

    thismonthfp = OrderDetail.objects.filter(creater__user__is_superuser=True).filter(status=6).filter(createtime__month=now.month).count() #本月分配
    thismonthrl =OrderDetail.objects.filter(createtime__month=now.month).filter(status=2).count()

    v1 = Order.objects.filter(status=6).filter(custome=user).count() #已安排治疗
    v2 = Order.objects.filter(status=11).filter(custome=user).count()
    v3 = Order.objects.filter(status=13).filter(custome=user).count()
    v4 = Order.objects.filter(status=12).filter(custome=user).count()

    todaywork = Order.objects.filter(nextcalldate__lte=now) #今日任务


    notify1 = Order.objects.exclude(Order__creater=user).filter(Order__is_operation=False) #管理员分配和销售备注
    notify2 = Order.objects.filter(nextcalldate__lte=yestoday.date())



    #identity=manag.usertype #身份(1,'客服')(2,'销售'),(3,'管理员')

    return  render(request,"index.html",{"user":user,"thismonth":thismonth,"thismonthfp":thismonthfp,"thismonthrl":thismonthrl,"v1":v1,"v2":v2,"v3":v3,"v4":v4,"todaywork":todaywork,"notify":notify1|notify2})

def orderlist(request):
    cusid= request.GET.get("cid")
    orders = Order.objects.filter(custome=cusid)




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

