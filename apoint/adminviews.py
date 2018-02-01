from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from apoint.models import ZJUser

#@login_required(login_url="/login/")
def staff(request):
    users = ZJUser.objects.all()
    return render(request,{"user":users})