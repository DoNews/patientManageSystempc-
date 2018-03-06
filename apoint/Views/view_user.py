#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,UserManager,User
from apoint.models import ZJUser
def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        url=""
        if user and user.is_active:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    url="/adminindex"
                else:
                    url = "/index"
                return HttpResponse('{"result":1,"url":"'+url+'"}')
            else:
                return HttpResponse('{"result":0}')
        else:

            return HttpResponse('{"result":0}')
    else:
        return render(request,"login.html")
    return render(request, "login.html")

def createUser(request):
    username =request.POST.get("username")
    name = request.POST.get("name")
    password = request.POST.get("pwd")
    phone= request.POST.get("phone")
    user = User(username=username)
    user.set_password(password)
    user.is_superuser=False
    user.is_active = True
    user.first_name=name
    user.is_staff=True
    # user.profile.name=name
    user.save()
    ZJUser(user=user,name=name,usertype=1,phone=phone).save()
    return HttpResponse({"result":1,"msg":"OK"})

