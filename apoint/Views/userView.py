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
        print user
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
    return render(request, "login.html")


def createUser(request):
    username =request.POST.get("username")
    name = request.POST.get("name")
    password = request.POST.get("pwd")
    user = User(username=username)
    user.set_password(password)
    user.is_superuser=False
    user.is_active = True
    user.is_staff=True
    # user.profile.name=name
    user.save()
    ZJUser(user=user,name=name,usertype=1).save()
    return HttpResponse("OK")
