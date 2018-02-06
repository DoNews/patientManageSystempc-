#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from apoint.models import ZJUser

#@login_required(login_url="/login/")
def staff(request):
    users = ZJUser.objects.all()
    return render(request,{"user":users})


MENUS_CALLER=(
    ("员工管理","/adminindex"),
    ("患者管理","/pationsview"),
    ("提醒管理","/remind"),
    ("报表管理","/chart"),
    ("账户管理","/account")

)
def adminindex(request):
    return render(request,"adminindex.html",{"pageindex":0})

def pations(request):
    return render(request,"admin/admindataManage.html",{"pageindex":1})

def hospital(request):
    return render(request,"admin/adminHospitalManage.html",{"pageindex":2})

def thirdpart(request):
    return render(request, "admin/adminAnontherSystem.html",{"pageindex":3})
def chart(request):
    return render(request, "admin/adminAnontherSystem.html",{"pageindex":4})
def account(request):
    return render(request, "admin/adminAnontherSystem.html",{"pageindex":5})