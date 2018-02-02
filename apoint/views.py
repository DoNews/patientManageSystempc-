#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required, user_passes_test
from datetime import datetime, timedelta
from apoint.common import *
# Create your views here.
from models import *
def checkUser():
    pass

MENUS_CALLER=(
    ("控制台","/index"),
    ("患者管理","/pationsview"),
    ("提醒管理","/remind"),
    ("报表管理","/"),
    ("账户管理","/account")

)

@login_required(login_url="/login/")
def index(request):
    # print "拿到的是什么",request.user.is_active
    #all_datas = YourModel.objects.filter(time__year=now_time.year) #查询某年的
    #all_datas = YourModel.objects.filter(time__month=now_time.month)#查询当前月份的
    user=ZJUser.objects.get(user=request.user)
    print "user:",request.user
    now =datetime.datetime.now()
    yestoday = now- timedelta(days=1)
    thismonth=OrderDetail.objects.filter(creater=user).filter(createtime__month=now.month).count()#本月跟进工单

    thismonthfp = OrderDetail.objects.filter(creater__user__is_superuser=True).filter(status=6).filter(createtime__month=now.month).count() #本月分配
    thismonthrl =OrderDetail.objects.filter(createtime__month=now.month).filter(status=2).count()

    v1 = OrderDetail.objects.filter(status=6).filter(creater=user).count() #已安排治疗
    v2 = OrderDetail.objects.filter(status=11).filter(creater=user).count()
    v3 = OrderDetail.objects.filter(status=13).filter(creater=user).count()
    v4 = OrderDetail.objects.filter(status=12).filter(creater=user).count()

    todaywork = Order.objects.filter(nextcalldate__lte=now,custome=user) #今日任务

    renling = Order.objects.filter(status=1,custome__isnull=True)
    notify1 = Order.objects.exclude(Order__creater=user).filter(Order__is_operation=False,custome=user) #管理员分配和销售备注
    notify2 = Order.objects.filter(nextcalldate__lte=yestoday.date(),custome=user)



    #identity=manag.usertype #身份(1,'客服')(2,'销售'),(3,'管理员')

    return  render(request,"index.html",{"user":user,"thismonth":thismonth,"thismonthfp":thismonthfp,"thismonthrl":thismonthrl,"v1":v1,"v2":v2,"v3":v3,"v4":v4,"todaywork":todaywork,"notify":(notify1|notify2).distinct(),"renling":renling,"pageindex":0,"menu":MENUS_CALLER})

@login_required(login_url="/login/")
def renling(request):
    sid = request.GET.get("id")
    order = Order.objects.filter(pk=sid).first()
    hosp = Hospital.objects.all()
    area = Area.objects.all()
    return render(request,"hzrlpop.html",{"order":order,"hosp":hosp,"area":area})

@login_required(login_url="/login/")
def renlingAction(request):
    sid =request.POST.get("sid")
    order = Order.objects.get(pk=sid)
    if order.custome:
        return HttpResponse("{\"result\":-1,\"msg\":\"已经被认领\"}")
    customer = ZJUser.objects.get(user=request.user)
    order.custome=customer
    order.nextcalldate =datetime.datetime.now().date()
    order.status=2
    order.save()
    OrderDetail(order=order,creater=customer,createtime=datetime.datetime.now(),status=2,remark="认领").save()
    return JsonResutResponse({"result":1,"msg":"认领成功"})

def orderlist(request):
    cusid= request.GET.get("cid")
    orders = Order.objects.filter(custome=cusid)

def pationsview(request):
    user = request.user
    cus = ZJUser.objects.filter(user=user)
    orders = Order.objects.filter(custome=cus).order_by("-wantTime")
    return render(request,"patientManage.html",{"order":orders,"pageindex":1,"menu":MENUS_CALLER})

@login_required(login_url="/login/")
def pations(request):
    user = request.user
    cus = ZJUser.objects.filter(user=user)
    orders = Order.objects.filter(custome=cus).order_by("-wantTime")
    return JsonResutResponse({"result":1,"list":list(orders)})

@login_required(login_url="/login/")
def remind(request):
    user = ZJUser.objects.get(user=request.user)
    orders = Order.objects.filter(custome=user).order_by('-createtime')  # 查看逾期
    remin = Order.objects.filter(custome=user).filter(Order__creater__usertype=2).filter(
        Order__is_operation=False).order_by('-createtime')  # 所有备忘
    admin = Order.objects.filter(custome=user).filter(Order__creater__user__is_superuser=True).filter(
        Order__is_operation=False).order_by('-createtime')  # 查看分配
    if orders:
        lister = RemindSystem(orders[:4])  # 这是逾期的
    else:
        lister = []
    if remin:
        notes = ViewCheat(remin[:3])  # 这里是备忘
    else:
        notes = []
    if admin:
        admins = AdminDis(admin[:3])  # 这里是管理员分配的
    else:
        admins = []
    return render(request, "remindManage.html",
                  {'ret': 0, 'msg': 'success', 'lister': lister, 'notes': notes, 'admin': admins,"pageindex":2,"menu":MENUS_CALLER})
    return render(request,"remindManage.html",{"pageindex":2,"menu":MENUS_CALLER,"orders":orders,"remin":remin,"admin":admin})

def account(request):

    return render(request,"accountManage.html")