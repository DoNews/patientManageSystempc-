#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from models import *
from common import *
import functools, random
import requests
import json

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
    hospts=Hospital.objects.filter(sales=user)
    orders=Order.objects.filter(wanthospital__in=hospts).exclude(status=1).order_by('-createtime') #找到所有的订单
    lister = []
    if orders:
        for order in orders:
            data={
                'id':order.id,
                'name':order.name,#患者姓名
                'sex':order.sex,#性别
                'hospital':order.wanthospital.name,#预约医院
                'wantTime':order.wantTime.strftime('%Y-%m-%d')
            }
            lister.append(data)
    else:
        pass
    return JsonResutResponse({'ret':0,'msg':'success','lister':lister})

#查看患者详情
def PatientsDetail(request):
    id =request.GET.get('id')#拿到orderid
    order=Order.objects.get(id=id) #找到订单
    cust=order.custome #找到所属客服
    follows=OrderDetail.objects.filter(creater=cust,order=order)
    imgs=IllnessImage.objects.filter(patient=order) #找到患者上传的图片
    lister=[] #照片
    record=[]
    if imgs:
        for img in imgs:
            lister.append(img.image)
    else:
        pass
    if follows:
        for follow in follows:
            date={
                'name':follow.creater.name,#客服姓名
                'remark':follow.remark,#描述
                'time':follow.createtime.strftime('%Y-%m-%d %H:%M')
            }
            record.append(date)
    else:
        pass
    data={
        'id':order.id,
        'name':order.name,#名称
        'birthday':order.birthday.strftime('%Y-%m-%d'),#出生日期
        'sex':order.sex,#性别
        'phone':order.phone,#手机
        'area':order.area.name,#区域
        'wantTime':order.wantTime.strftime('%Y-%m-%d'),#预约时间
        'wanthospital':order.wanthospital.name,#医院
        'description':order.description,#胎记描述
        'photo':lister, #照片
    }
    return JsonResutResponse({'ret':0,'msg':'success','data':data,'customer':record,})

#员工提交备忘录
def TheMemo(request):
    id =request.POST['id'] #orderid
    openid=request.POST['openid'] #员工的openid
    seles=SalesUser.objects.filter(openid=openid).first() #找到员工
    describe=request.POST['describe'] #描述
    types=request.POST['types']
    order=Order.objects.filter(id=id).first()
    OrderDetail.objects.create(order=order,creater=seles,status=int(types),remark=describe)
    return JsonResutResponse({'ret':0,'msg':'success'})

#患者点击预约
def CilckMake(request):
    openid=request.GET.get('openid')
    order=Order.objects.filter(openid=openid)
    if order:
        return JsonResutResponse({'ret':1,'msg':'已经有预约正在进行中'})
    else:
        return JsonResutResponse({'ret':0,'msg':'success'})

#患者order提交
def OrderSubmit(request):
    item={}
    for key in request.POST:
        if key=='name':
            name=request.POST[key]
            item['name']=request.POST[key]
        elif key=='phone':
            phone=request.POST[key]
            item[key]=request.POST[key]
        elif key=='area':
            area=Area.objects.filter(id=request.POST[key]).first()
            item['area']=area
        elif key=='hospital':
            hospital=Hospital.objects.filter(id=request.POST[key]).first()
            item['wanthospital']=hospital
        elif key =='photo':
            photo=request.POST[key]
        else:
            if request.POST[key]:
                item[key] = request.POST[key]
    photos = json.loads(photo)  # 图片
    order=Order.objects.filter(name=name,phone=phone)
    if order:
        return JsonResutResponse({'ret':1,'msg':'已有预约正在进行中'})
    else:
        order=Order.objects.create(**item)
    for photo in photos:
        IllnessImage.objects.create(image=photo,patient=order)
    return JsonResutResponse({'ret':0,'msg':'success'})



# 上传图片
def uploader(request):
    img = request.FILES.get('img')
    img_url = Compression(img)
    return HttpResponse(simplejson.dumps({"result": 0, "imgurl": img_url}))

#所有省
def Province(request):
    provs=Area.objects.all()
    lister=[]
    if provs:
        for prov in provs:
            data={
                'id':prov.id,
                'name':prov.name,
                'value':prov.name,
            }
            lister.append(data)
    else:
        pass
    return JsonResutResponse({'ret':0,'msg':'success','lister':[lister]})

#医院
def Hospitaltable(request):
    hospits=Hospital.objects.all()
    lister=[]
    if hospits:
        for hosp in hospits:
            data={
                'id':hosp.id,
                'name':hosp.name,
                'value':hosp.name,
            }
            lister.append(data)
    else:
        pass
    return JsonResutResponse({'ret':0,'msg':'success','lister':[lister]})
