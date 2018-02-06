#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from apoint.models import ZJUser

#@login_required(login_url="/login/")
def staff(request):
    users = ZJUser.objects.all()
    return render(request,{"user":users})



def adminindex(request):
    return render(request,"adminindex.html",{"pageindex":0})

def pations(request):
    return render(request,"admin/admindataManage.html",{"pageindex":1})

def hospital(request):
    return render(request,"admin/adminHospitalManage.html",{"pageindex":2})

def thirdpart(request):
    return render(request, "admin/adminAnontherSystem.html",{"pageindex":3})
def adminchart(request):
    return render(request, "admin/adminreportFormManage.html",{"pageindex":4})
def accountview(request):
    return render(request, "admin/adminAccountManage.html",{"pageindex":5})