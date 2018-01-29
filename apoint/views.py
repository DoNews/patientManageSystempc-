#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required, user_passes_test
# Create your views here.
from models import *
def checkUser():
    pass

@login_required(login_url="/login/")
def index(request):
    # print "拿到的是什么",request.user.is_active
    manag=ZJUser.objects.filter(user=request.user).first() #找到登陆者
    identity=manag.usertype #身份(1,'客服')(2,'销售'),(3,'管理员')
    return  render(request,"index.html")

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

