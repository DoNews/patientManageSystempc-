#coding: utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from apoint.models import *
from apoint.common import *
from django.utils import timezone
from apoint.task import *
import functools, random
import requests
import json

#发验证码
def ScrfCode(request):
  tele = request.POST['phone']
  n = functools.reduce(lambda x, y: 10 * x + y, [random.randint(1, 4) for x in range(4)])
  http = "http://222.73.117.158:80/msg/HttpBatchSendSM"
  r=requests.post(http, {"account": "muai37", "pswd": "Muai888123", "mobile": "%s" % tele, "msg": "您的验证码是%s" % n,"needstatus": "false"})
  request.session["code"] = n
  return JsonResutResponse({'ret': 0,'msg':'success'})

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
            user.openid=openid
            user.is_cert=True
            user.email=email
            user.save()
            return JsonResutResponse({"ret": 0,'msg':'success'})
        else:
            return JsonResutResponse({'ret':1,'msg':u'手机号或姓名不匹配'})

#我负责的患者（销售）
def MyPatients(request):
    openid=request.GET.get('openid')
    user=SalesUser.objects.filter(openid=openid).first() #找到员工
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
    data,record,is_end=Detail(order)
    return JsonResutResponse({'id':id,'ret':0,'msg':'success','data':data,'customer':record,'is_end':is_end})

#查看所有详情
def LookCheat(request):
    id=request.GET.get('id')
    order = Order.objects.get(id=id)  # 找到订单
    follows = OrderDetail.objects.filter(order=order)
    record = []
    for follow in follows:
        date = {
            'name': follow.creater.name if follow.creater else '',  # 客服姓名
            'remark': follow.remark,  # 描述
            'time': follow.createtime.strftime('%Y-%m-%d %H:%M')
        }
        record.append(date)
    return JsonResutResponse({'ret':0,'msg':'success','customer':record,})
#判断是否有预约
def checkphone(request):
    phone = request.GET.get("phone",False)
    if phone:
        u = Order.objects.filter(phone=phone).first()
        if u:
          return JsonResutResponse({'ret':1,'msg':'您有预约正在流程中，无需再次预约','oepnid':u.openid})
    return JsonResutResponse({'ret':0,'msg':'无预约'})

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
    openid=request.GET.get('openid',None)
    order=Order.objects.filter(openid=openid)
    if order:
        return JsonResutResponse({'ret':1,'msg':'已经有预约正在进行中','openid':openid})
    else:
        return JsonResutResponse({'ret':0,'msg':'success'})

#微信患者order提交
def PhoneOrder(request):
    userinfo=request.POST['userinfo']
    photo=request.POST['photo']
    codes = request.POST['codes']
    code = request.session.get("code")
    user=json.loads(userinfo) #用户
    photos = json.loads(photo)  # 图片
    item={}
    for k in user:
        if k=='name':
            item[k]=user[k]
        elif k=='wanthospital':
            hosp=Hospital.objects.filter(id=user[k]).first()
            item[k]=hosp
        elif k=='phone':
            phone=user[k]
            item[k]=user[k]
        elif k=='area':
            area=Area.objects.filter(id=user[k]).first()
            item[k]=area
        else:
            item[k]=user[k]
    orderser=Order.objects.filter(phone=phone)
    if orderser:
        return JsonResutResponse({'ret':1,'msg':'已有预约正在进行中'})
    else:
        if code == int(codes):
            orders = Order.objects.all()
            n = len(orders) + 1
            s = "NO.%04d" % n
            item['serial'] = s
            order = Order.objects.create(**item)
        else:
            return JsonResutResponse({'ret': 2, 'msg': '验证码不正确'})
    for photo in photos:
        IllnessImage.objects.create(image=photo,patient=order)
    try:
        ModelMsg(order.id, 1, 1)
    except:
        return HttpResponse("模板消息发送失败，因为没有模板ID")
    return JsonResutResponse({'ret':0,'msg':'success'})

#患者详情
def OrderDeta(request):
    openid=request.GET.get('openid')
    order=Order.objects.filter(openid=openid).first()
    data, record, is_end = Detail(order)
    return JsonResutResponse({'id': order.id, 'ret': 0, 'msg': 'success', 'data': data, 'customer': record, 'is_end': is_end})


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
    lister=[]
    areas=Area.objects.all() #所有的省
    if areas:
        for area in areas:
            data={
                'name':area.name,# 省的名称
                'value':'%s'%area.id,#省的id
                'parent':'%s'%0,
            }
            lister.append(data)
            data={
                'name':'期望预约医院',
                'value':'%s'%999,
                'parent':'%s'%area.id,
            }
            lister.append(data)
            hospits=Hospital.objects.filter(province=area)
            if hospits:
                for hosp in hospits:
                    data={
                        'parent':'%s'%area.id,
                        'name':hosp.name,
                        'value':'%s'%hosp.id,
                    }
                    lister.append(data)
            else:
                pass
    else:
        pass
    return JsonResutResponse({'ret':0,'msg':'success','lister':[lister]})

#给第三方使用的接口 #状态 改成已治疗
def ThirdParty(request):
    data=request.POST['data']
    users=json.loads(data)
    try:
        for user in users:
            name=user['name'] #姓名
            sex=user['sex'] #性别
            birthday=user['birthday']
            phone=user['phone'] #手机号
            wantTime=user['wantTime'] #治疗时间
            city=user['city']#城市
            hospital=user['hospital'] #医院
            ordertype=user['ordertype'] #订单状态
            change_time=user['change_time'] #变更时间
            hosps=Hospital.objects.filter(name=hospital).first() #判断是否有这个医院
            if hosps:
                hos =hosps
            else:
                hos=Hospital.objects.create(name=hospital)
            are=Area.objects.filter(name=city).first()
            if are:
                area=are
            else:
                area=Area.objects.create(name=city)
            use=Order.objects.filter(phone=phone).first()
            if use:
                use.name=name
                use.wantTime=wantTime
                use.area=area
                use.wanthospital=hos
                use.ordertype=ordertype
                use.three_time=change_time
                use.number+=1
                use.status=6
                use.save()
                usesr=use
            else:
                orders = Order.objects.all()
                n = len(orders) + 1
                s = "NO.%04d" % n
                usesr=Order.objects.create(name=name,sex=sex,wantTime=wantTime,area=area,wanthospital=hos,number=1,status=6,phone=phone,is_party=True,birthday=birthday,serial=s,three_time=change_time,ordertype=ordertype)
            OrderDetail.objects.create(order=usesr,status=6,remark='第三方导入')
        return JsonResutResponse({'ret':0,'msg':'success'})
    except:
        return JsonResutResponse({'ret':1,'msg':'error'})

#患者搜索
def PatSearch(request):
    name=request.GET.get('name')
    openid=request.GET.get('openid')
    user=SalesUser.objects.filter(openid=openid).first()
    hosps=Hospital.objects.filter(sales=user) #找到所有的医院
    orders=Order.objects.filter(wanthospital__in=hosps,name__icontains=name)
    lister=[]
    if orders:
        for order in orders:
            data = {
                'id': order.id,
                'name': order.name,  # 患者姓名
                'sex': order.sex,  # 性别
                'hospital': order.wanthospital.name,  # 预约医院
                'wantTime': order.wantTime.strftime('%Y-%m-%d')
            }
            lister.append(data)
    else:
        pass
    return JsonResutResponse({'ret': 0, 'msg': 'success', 'lister': lister})
