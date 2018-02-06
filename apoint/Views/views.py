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
import json
from apoint.models import *
def checkUser():
    pass

MENUS_CALLER=(
    ("控制台","/index"),
    ("患者管理","/pationsview"),
    ("提醒管理","/remind"),
    ("报表管理","/chart"),
    ("账户管理","/account")

)

def chart(request):

    return render(request, "formManage.html", {"pageindex":3 , "menu":MENUS_CALLER})

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
    notify1 = Order.objects.filter(Order__creater__user__is_superuser=True).filter(Order__is_operation=False,custome=user) #管理员分配
    notify2= Order.objects.filter(Order__creater__usertype=2).filter(Order__is_operation=False,custome=user)#有备注
    notify3 = Order.objects.filter(nextcalldate__lte=yestoday.date(),custome=user) #逾期了

    arr=[]
    for n in notify1:
        dic ={}
        data = {
            'id': n.id,
            'name': n.name,
            'hosp': n.wanthospital,
            'time':n.wantTime,
            'type':1
        }
        if checkdicinlist(arr, n.id):
            arr.append(data)
    for n in notify2:
        dic ={}
        data = {
            'id': n.id,
            'name': n.name,
            'hosp': n.wanthospital,
            'time':n.wantTime,
            'type':2
        }
        if checkdicinlist(arr,n.id):
            arr.append(data)
    for n in notify3:
        dic ={}
        data = {
            'id': n.id,
            'name': n.name,
            'hosp': n.wanthospital,
            'time':n.wantTime,
            'type':3,
            'yuqu':(datetime.datetime.now().date()- n.nextcalldate).days
        }
        if checkdicinlist(arr, n.id):
            arr.append(data)
    #identity=manag.usertype #身份(1,'客服')(2,'销售'),(3,'管理员')
    print arr
    return  render(request, "index.html", {"user":user, "thismonth":thismonth, "thismonthfp":thismonthfp, "thismonthrl":thismonthrl, "v1":v1, "v2":v2, "v3":v3, "v4":v4, "todaywork":todaywork, "notify":arr, "renling":renling, "pageindex":0, "menu":MENUS_CALLER})

def checkdicinlist(arr,sid):
    for a in arr:
        if a['id']==sid:
            return False
    return True

@login_required(login_url="/login/")
def renling(request):
    sid = request.GET.get("id")
    order = Order.objects.filter(pk=sid).first()
    hosp = Hospital.objects.all()
    area = Area.objects.all()
    print order.pation.all()
    return render(request, "hzrlpop.html", {"order":order, "hosp":hosp, "area":area, 'imgs':order.pation.all()})

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
    return render(request, "patientManage.html", {"order":orders, "pageindex":1, "menu":MENUS_CALLER})

@login_required(login_url="/login/")
def pations(request):
    user = request.user
    cus = ZJUser.objects.filter(user=user)
    orders = Order.objects.filter(custome=cus).order_by("-wantTime")
    return JsonResutResponse({"result":1,"list":list(orders)})

@login_required(login_url="/login/")
def remind(request):
    user = ZJUser.objects.get(user=request.user)
    now = datetime.datetime.now()
    yestoday = now - timedelta(days=1)
    orders = Order.objects.filter(custome=user,nextcalldate__lte=yestoday.date(),nextcalldate__isnull=False).order_by('-createtime')
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
    return render(request, "remindManage.html", {"pageindex":2, "menu":MENUS_CALLER, "orders":orders, "remin":remin, "admin":admin})

def account(request):
    return render(request, "accountManage.html", {"pageindex":4, "menu":MENUS_CALLER})

def addpation(request):
    hosp = Hospital.objects.all()
    area = Area.objects.all()

    return render(request, "addpeople.html", {"hosp": hosp, "area": area})

@login_required(login_url="/login/")
def orderdetail(request):
    user = ZJUser.objects.get(user=request.user)
    id = request.GET.get('id')  # 患者订单的id
    order = Order.objects.filter(id=id).first()  # 患者订单
    imgs = IllnessImage.objects.filter(patient=order).values("image")  # 患者上传的图片

    follows = OrderDetail.objects.filter(order=order).order_by('-createtime')  # 对订单的所有操作
    if order.custome==user:
        follows.filter(is_operation=False).update(is_operation=True)
    hosp = Hospital.objects.all()
    area = Area.objects.all()

    return render(request, "OrderDetail.html", {"order":order, "imgs":imgs, "follows":follows, "iscreater": order.custome == user, "hosp":hosp, "area":area})

# 上传图片
def uploader(request):
    img = request.FILES.get('file')
    img_url = Compression(img)
    return HttpResponse(simplejson.dumps({"result": 0, "imgurl": img_url}))

@login_required(login_url="/login/")
def OrderSubmit(request):
    userinfo=request.POST['userinfo']
    photo=request.POST['photo']
    cid =request.user
    zuser = ZJUser.objects.filter(user=cid).first()
    print userinfo,photo
    user=json.loads(userinfo) #用户
    photos = json.loads(photo)  # 图片
    item={}
    for k in user:
        if k=='name':
            name=user[k]
            item[k]=user[k]
        elif k=='wanthospital':
            hosp=Hospital.objects.filter(id=user[k]).first()
            item[k]=hosp
        elif k=='phone':
            phone=user[k]
            item[k]=user[k]
        elif k=='area':
            area=Area.objects.filter(id=user[k]).first()
            item[k]=area
        else:
            item[k]=user[k]
    order=Order.objects.filter(name=name,phone=phone)
    if order:
        return JsonResutResponse({'ret':1,'msg':'已有预约正在进行中'})
    else:
        orders=Order.objects.all()
        n=len(orders)+1
        s = "NO.%04d" % n
        item['serial']=s
        item['custome_id']=zuser.id
        item["status"] =2
        order=Order.objects.create(**item)
    for photo in photos:
        IllnessImage.objects.create(image=photo,patient=order)
    return JsonResutResponse({'ret':0,'msg':'success'})

@login_required(login_url="/login/")
def OrderUpdte(request):
    userinfo=request.POST['userinfo']
    photo=request.POST['photo']

    folow=request.POST['folow']
    cid =request.user
    zuser = ZJUser.objects.filter(user=cid).first()

    user=json.loads(userinfo) #用户
    photos = json.loads(photo)  # 图片
    folows = json.loads(folow)
    item={}
    for k in user:
        if k=='name':
            name=user[k]
            item[k]=user[k]
        elif k=='wanthospital':
            hosp=Hospital.objects.filter(id=user[k]).first()
            item[k]=hosp
        elif k=='phone':
            phone=user[k]
            item[k]=user[k]
        elif k=='area':
            area=Area.objects.filter(id=user[k]).first()
            item[k]=area
        elif k=='oid':
            pass
        else:
            item[k]=user[k]
    order = Order.objects.filter(id=user['oid'])
    order.update(**item)
    IllnessImage.objects.filter(patient=order.first()).delete()
    for photo in photos:
        IllnessImage.objects.create(image=photo,patient=order.first())
    folowitem ={}
    for f in folows:
        folowitem[f]=folows[f]
    folowitem['order_id']=user['oid']
    folowitem['creater_id']=zuser.id

    OrderDetail.objects.create(**folowitem)
    return JsonResutResponse({'ret':0,'msg':'success'})