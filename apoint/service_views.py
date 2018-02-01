#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from models import *
from common import *
import functools, random
import requests
from datetime import datetime, timedelta
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
@login_required(login_url="/login/")
def Remind(request):
    user = ZJUser.objects.get(user=request.user)
    orders =Order.objects.filter(custome=user).order_by('-createtime') #查看逾期
    remin = Order.objects.filter(custome=user).filter(Order__creater__usertype=2).filter(
        Order__is_operation=False).order_by('-createtime') #所有备忘
    admin = Order.objects.filter(custome=user).filter(Order__creater__user__is_superuser=True).filter(Order__is_operation=False).order_by('-createtime') #查看分配
    if orders:
        lister=RemindSystem(orders[:4]) #这是逾期的
    else:
        lister=[]
    if remin:
        notes=ViewCheat(remin[:3]) #这里是备忘
    else:
        notes=[]
    if admin:
        admins=AdminDis(admin[:3]) #这里是管理员分配的
    else:
        admins=[]
    return JsonResutResponse({'ret':0,'msg':'success','lister':lister,'notes':notes,'admin':admins})

#查看所有逾期
@login_required(login_url="/login/")
def Remindall(request):
    user = ZJUser.objects.get(user=request.user)
    orders = Order.objects.filter(custome=user).order_by('-createtime')
    lister = RemindSystem(orders)
    return JsonResutResponse({'ret': 0, 'msg': 'success', 'lister': lister})

#查看所有备忘
@login_required(login_url="/login/")
def Cheatall(request):
    user = ZJUser.objects.get(user=request.user)
    orders=Order.objects.filter(custome=user).filter(Order__creater__usertype=2).filter(
        Order__is_operation=False).order_by('-createtime')
    notes=ViewCheat(orders)
    return JsonResutResponse({'ret':0,'msg':'success','notes':notes})

#查看所有管理员分配
@login_required(login_url="/login/")
def Adminsall(request):
    user = ZJUser.objects.get(user=request.user)
    orders=Order.objects.filter(custome=user).filter(Order__creater__user__is_superuser=True).filter(Order__is_operation=False).order_by('-createtime')
    admins=AdminDis(orders)
    return JsonResutResponse({'ret': 0, 'msg': 'success', 'admins': admins})

#客服的数据统计
@login_required(login_url="/login/")
def Statistics(request):
    user = ZJUser.objects.get(user=request.user)
    now = datetime.datetime.now()
    thismonthfp=OrderDetail.objects.filter(creater__user__is_superuser=True,order__custome=user,createtime__month=now.month) #查看本月分配的数据
    thismonth = OrderDetail.objects.filter(creater=user).filter(createtime__month=now.month).count() #本月累计跟进人次
    thismonthrl = OrderDetail.objects.filter(createtime__month=now.month).filter(status=2).count() #本月认领
    v1 = OrderDetail.objects.filter(status=6,createtime__month=now.month).filter(custome=user).count()#本月已安排治疗
    v2 = OrderDetail.objects.filter(status=11,createtime__month=now.month).filter(custome=user).count() #延后治疗
    v3 = OrderDetail.objects.filter(status=13,createtime__month=now.month).filter(custome=user).count() #转院的
    v4 = OrderDetail.objects.filter(status=12,createtime__month=now.month).filter(custome=user).count() #暂停的
    #查看全部
    thismonthall = OrderDetail.objects.filter(creater=user).count()  # 全部累计跟进人次
    thismonthfpall = OrderDetail.objects.filter(creater__user__is_superuser=True,order__custome=user)#查看全部分配的数据
    thismonthrlall = OrderDetail.objects.filter(status=2).count()  # 全部认领
    v1all = OrderDetail.objects.filter(status=6,custome=user).count()  # 全部已安排治疗
    v2all = OrderDetail.objects.filter(status=11,custome=user).count()  # 全部延后治疗
    v3all = OrderDetail.objects.filter(status=13,custome=user).count()  # 全部转院的
    v4all = OrderDetail.objects.filter(status=12,custome=user).count()  # 全部暂停的
    return render(request,'.html',{'thismonth':thismonth,'thismonthfp':thismonthfp,'thismonthrl':thismonthrl,'v1':v1,'v2':v2,'v3':v3,'v4':v4,'thismonthall':thismonthall,'thismonthfpall':thismonthfpall,'thismonthrlall':thismonthrlall,'v1all':v1all,'v2all':v2all,'v3all':v3all,'v4all':v4all})

#客服账户设置
def AccountSet(request):
    id=request.POST['id'] #客服的id
    oldpass=request.POST['oldpass'] #当前密码
    newpass=request.POST['newpass'] #新密码
    conpass=request.POST['conpass'] #确认密码
    user=ZJUser.objects.get(id=id)
    if user.user.check_password(oldpass)==True and newpass==conpass:
        user.user.set_password(newpass)
        return JsonResutResponse({'ret':0,'msg':u'设置成功'})
    else:
        return JsonResutResponse({'ret':1,'msg':u'密码错误/新密码和确认密码不匹配'})

#管理员的员工管理
@login_required(login_url="/login/")
def StafManag(request):
    user = ZJUser.objects.get(user=request.user)
    if user.user.is_superuser==True:
        users=SalesUser.objects.all().order_by('-createtime') #找的是员工
        if users:
            staffs=users[:9]
        else:
            staffs=[]
        ser=ZJUser.objects.filter(usertype=1) #找的是客服
        if ser :
            services=ser[:2]
        else:
            services=[]
        return render(request,'xxxx.html',{'staffs':staffs,'service':services})
    else:
        return HttpResponse(u"你不是管理员，无权查看")
#点击查看所有员工
def StaffAll(request):
    page=request.POST['page']
    staffs=SalesUser.objects.all().order_by('-createtime')
    result, contacts = Paging(staffs, page)
    lister=[]
    for staff in contacts:
        data={
            'id':staff.id,
            'name':staff.name,
            'phone':staff.phone,
            'is_cert':staff.is_cert,#绑定状态
            'city':staff.city,
            'director':staff.director,#主管
        }
        lister.append(data)
    return JsonResutResponse({'ret':0,'msg':'success','lister':lister,'result':result})
#点击查看所有销售
def ServiceAll(request):
    page = request.GET.get('page')
    services = ZJUser.objects.filter(usertype=1)  # 找的是客服
    result, contacts = Paging(services, page)
    lister=[]
    for serv in contacts:
        data={
            'id':serv.id,
            'name':serv.name,
            'username':serv.user.username,#账号
        }
        lister.append(data)
    return JsonResutResponse({'ret':0,'msg':'success','lister':lister,'result':result})
#查看员工详情
def StaffEditor(request):
    id=request.GET.get('id') #员工的id
    user=SalesUser.objects.get(id=id)
    hosps=Hospital.objects.filter(sales=user)#对应的医院
    return render(request,'xxxx.html',{'user':user,'hosps':hosps})

#添加员工和修改员工
def AddStaff(request):
    name=request.POST['name']
    phone=request.POST['phone'] #电话
    director=request.POST['director'] #主管
    city=request.POST['city'] #城市
    hosps=request.POST['hosps'] #所有医院的id
    user=SalesUser.objects.filter(name=name,phone=phone)
    if user:
        staff=user.update(name=name,phone=phone,director=director,usertype=2,city=city)
    else:
        staff=SalesUser.objects.create(name=name,phone=phone,director=director,usertype=2,city=city)
    hospser = json.loads(hosps) #医院的id
    for hos in hospser:
        Hospital.objects.filter(id=hos).update(sales=staff)
    return HttpResponse(u'添加成功')

#查询医院(一省对应一个医院列表)
def QueryHosp(request):
   areas=Area.objects.all() #所有的省
   lister=[]
   for area in areas:
       hosp=Hospital.objects.filter(province=area)
       data={
           'area':area.name,
           'hopsital': list(hosp),
       }
       lister.append(data)
   return JsonResutResponse({'ret':0,'msg':'success','lister':lister})


#删除
def StaffDelete(request):
    id=request.POST['id']
    ZJUser.objects.get(id=id).delete()
    return render(request,'xxxx.html',{'msg':u'删除成功'})



#管理员数据管理
def AdminData(request):
    order=Order.objects.all().order_by('-createtime') #患者
    hosp=Hospital.objects.all().order_by('-createtime') #医院
    noservit=Order.objects.filter(is_party=True,custome=None).order_by('-createtime')#第三方进来的 没有客服的
    if order:
        orders=order[:6]
    else:
        orders=[]
    if hosp:
        hosption=hosp[:3]
    else:
        hosption=[]
    if noservit:
        foreign=noservit[:3]
    else:
        foreign=[]
    return render(request, 'xxx.html',{'orders':orders,'hosption':hosption,'foreign':foreign})

#查看所有患者
def OrderAll(request):
    page=request.GET.get('page')
    orders=Order.objects.all().order_by('-createtime')
    result,contacts = Paging(orders, page)
    lister=[]
    for order in contacts:
        data={
            'id':order.id,
            'name': order.name,  # 患者姓名
            'wanthospital': order.wanthospital.name,  # 医院名称
            'wantTime': order.wantTime.strftime('%Y-%m-%d  %H:%M'),  # 预约时间
            'custome':order.custome.name,#负责客服
            'sales': order.wanthospital.sales.name,  # 负责销售
            'status':order.get_status_display(),#当前状态
            'is_party':order.is_party,#是否是第三方
        }
        lister.append(data)
    return JsonResutResponse({'ret':0,'msg':'success','lister':lister,'result':result})

#查看全部医院
def Allhospit(request):
    page=request.GET.get('page')
    hospits=Hospital.objects.all().order_by('-createtime')
    result, contacts = Paging(hospits, page)
    lister = []
    for hosp in contacts:
        data={
            'id':hosp.id,
            'area':hosp.province,
            'name':hosp.name
        }
        lister.append(data)
    return JsonResutResponse({'ret':0,'msg':'success','lister':lister,'result':result})

#医院的去管理的详情页
def HospitMent(request):
    pass