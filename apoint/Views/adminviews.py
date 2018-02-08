#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from apoint.models import ZJUser,SalesUser
from apoint.common import *
from django.contrib.auth.decorators import login_required
#@login_required(login_url="/login/")
def staff(request):
    users = ZJUser.objects.all()
    return render(request,{"user":users})


@login_required(login_url="/login/")
def adminindex(request):
    page=request.GET.get('page',1)
    user = ZJUser.objects.get(user=request.user)
    users=SalesUser.objects.all().order_by('-createtime') #找的是员工
    result, contacts = Paging(users, page)
    lister = []
    for staff in contacts: #销售的要分页
        hosps = Hospital.objects.filter(sales=staff)
        citys=''
        for h in hosps:
            if citys.find(h.province.name)>-1:
                continue
            citys=citys+h.province.name + " "
        data = {
            'id': staff.id,
            'name': staff.name,
            'phone': staff.phone,
            'is_cert': staff.is_cert,  # 绑定状态
            'city': citys,
        }
        lister.append(data)
    ser=ZJUser.objects.filter(usertype=1) #找的是客服

    return render(request, "admin/adminindex.html", {"pageindex":0,'staffs':lister,'service':ser})

def adminpationsview(request):
    orders = Order.objects.all()
    order = orders[:10]
    print orders
    return render(request,"admin/admindataManage.html",{"pageindex":1,"all":orders.count(),"order":order})

def hospital(request):

    hosp = Hospital.objects.all()
    hosps=[]
    for h in hosp:
        count = Order.objects.filter(wanthospital=h).count()
        hosps.append({"hosp":h,"count":count})
    return render(request,"admin/adminHospitalManage.html",{"pageindex":2,"hosp":hosps})

def thirdpart(request):
    noservit = Order.objects.filter(is_party=True, custome=None).order_by('-createtime').count()  # 第三方进来的 没有客服的
    return render(request, "admin/adminAnontherSystem.html",{"pageindex":3,"all":noservit})
def adminchart(request):
    return render(request, "admin/adminreportFormManage.html",{"pageindex":4})
def adminaccount(request):
    return render(request, "accountManage.html",{"pageindex":5})
def staffedit(request):
    return render(request,"admin/addStaff.html",)
def editHospital(request):
    uid =request.GET.get("id")
    area = Area.objects.all()
    data =[]
    for a in area:
        hos=Hospital.objects.filter(province=a)
        u = SalesUser.objects.get(id=uid)
        g = hos.filter(sales=u)
        ishave =0
        if g:
            ishave=1
        data.append({"hosp":hos,"name":a.name,"id":a.id,"ishave":ishave})
    return render(request,"admin/editHospital.html",{"area":data,"uid":int(uid)})
def newStaffHosp(request):
    area = Area.objects.all()
    data = []
    for a in area:
        hos = Hospital.objects.filter(province=a)
        data.append({"hosp": hos, "name": a.name, "id": a.id})
    return render(request, "admin/addHospital.html", {"area": data})


def hospview(request):
    hid = request.GET.get("id",False)
    area = Area.objects.all()
    sales = SalesUser.objects.all()
    dit ={"area":area,"sales":sales}
    if hid:
        hos=Hospital.objects.get(pk=hid)
        dit={"area":area,"sales":sales,"hosp":hos}


    return render(request,"admin/adminHospitalManagePop.html",dit)

def thirdpop(request):
    nid = request.GET.get("id")
    oid=request.GET.get("oid")
    oorder=None
    if oid:
        oorder=Order.objects.get(pk=oid)
    if nid:
        norder=Order.objects.get(pk=nid)
    return render(request,"admin/thirdpop.html",{"o":oorder if oid else "","n":norder})

def refenpei(request):
    kefu = ZJUser.objects.filter(usertype=1)
    return render(request,"admin/redistribution.html",{"kefu":kefu})

def addCustomer(request):
    cid = request.GET.get("id",False)
    if cid:
        c = ZJUser.objects.get(pk=cid)
    return render(request,"admin/addCustom.html",{"c":c if cid else ""})

#添加客服账号
def addCustomerAction(request):
    name = request.POST.get("name")
    username = request.POST.get("username")
    phone=request.POST.get("phone")
    password = request.POST.get("pwd")

    id =request.POST.get("id")
    if id:
        kf = ZJUser.objects.get(pk = id)
        kf.name = name
        kf.user.username = username
        kf.phone = phone
        kf.user.set_password(password)
        kf.usertype = 1
        kf.user.save()
        kf.save()
    else:
        user = User(username=username)
        user.set_password(password)
        user.is_superuser = False
        user.is_active = True
        user.first_name = name
        user.is_staff = True
        # user.profile.name=name
        user.save()
        ZJUser(user=user, name=name, usertype=1, phone=phone).save()
        return  HttpResponse('{"result":1,"msg":"成功"}')

