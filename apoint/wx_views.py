#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from models import *
from common import *
import functools, random
import requests

#发验证码
def ScrfCode(request):
  tele = request.POST['phone']
  n = functools.reduce(lambda x, y: 10 * x + y, [random.randint(1, 4) for x in range(4)])
  http = "http://222.73.117.158:80/msg/HttpBatchSendSM"
  r=requests.post(http, {"account": "muai37", "pswd": "Muai888123", "mobile": "%s" % tele, "msg": "您的验证码是%s" % n,
                       "needstatus": "false"})
  request.session["code"] = n
  return JsonResutResponse({'ret': 0, })

#员工认证
def StaffCation(request):
    openid = request.POST['openid']
    realname = request.POST['name']
    email = request.POST['email']
    telephone = request.POST['phone']
    vercode = request.POST['vercode']  # 验证码
    code = request.session.get("code")
    total = SalesUser.objects.filter(openid=openid).first()
    if total:
        return JsonResutResponse({"ret": -1, "msg": u"你已经认证过"})
    else:
        user = SalesUser.objects.filter(name=realname, phone=telephone,).first()
        if user and code == int(vercode):
            user.is_cert=True
            user.email=email
            user.save()
            return JsonResutResponse({"ret": 0,'msg':'success'})
        else:
            return JsonResutResponse({'ret':1,'msg':u'手机号或姓名不匹配'})

#我负责的患者（销售）
def MyPatients(request):
    openid=request.GET.get('openid')
    user=SalesUser.objects.filter(openid=openid).first() #扎到员工
    orders=Order.objects.filter(sales=user).order_by('-createtime') #找到所有的订单
    lister = []
    if orders:
        for order in orders:
            data={
                'id':order.id,
                'name':order.name,#患者姓名
                'sex':order.sex,#性别
                'hospital':order.wanthospital,#预约医院
                'wantTime':order.wantTime.strftime('%Y-%m-%d')
            }
            lister.append(data)
    else:
        pass
    return JsonResutResponse({'ret':0,'msg':'success','lister':lister})
#查看患者详情
def PatientsDetail(request):
    id =request.GET.get('id')#拿到orderid
    order=Order.objects.get(id=id)
