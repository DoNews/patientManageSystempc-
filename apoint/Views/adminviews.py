#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from apoint.models import ZJUser,SalesUser
from apoint.common import *

#@login_required(login_url="/login/")
def staff(request):
    users = ZJUser.objects.all()
    return render(request,{"user":users})



def adminindex(request):
    page=request.GET.get('page')
    user = ZJUser.objects.get(user=request.user)
    users=SalesUser.objects.all().order_by('-createtime') #找的是员工
    result, contacts = Paging(users, page)
    lister = []
    for staff in contacts: #销售的要分页
        data = {
            'id': staff.id,
            'name': staff.name,
            'phone': staff.phone,
            'is_cert': staff.is_cert,  # 绑定状态
            'city': staff.city,
        }
        lister.append(data)
    ser=ZJUser.objects.filter(usertype=1) #找的是客服

    return render(request, "admin/adminindex.html", {"pageindex":0,'staffs':lister,'service':ser})

def pations(request):
    return render(request,"admin/admindataManage.html",{"pageindex":1})

def hospital(request):
    return render(request,"admin/adminHospitalManage.html",{"pageindex":2})

def thirdpart(request):
    return render(request, "admin/adminAnontherSystem.html",{"pageindex":3})
def adminchart(request):
    return render(request, "admin/adminreportFormManage.html",{"pageindex":4})
def adminaccount(request):
    return render(request, "admin/adminAccountManage.html",{"pageindex":5})