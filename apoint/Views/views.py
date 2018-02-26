# coding: utf8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django import template
from datetime import datetime, timedelta
from apoint.common import *
import requests
# Create your views here.
import json
from apoint.models import *


def checkUser():
    pass


MENUS_CALLER = (
    ("控制台", "/index"),
    ("患者管理", "/pationsview"),
    ("提醒管理", "/remind"),
    ("报表管理", "/chart"),
    ("账户管理", "/account")
)


@login_required(login_url="/login/")
def chart(request):
    user = ZJUser.objects.get(user=request.user)
    now = datetime.datetime.now()
    thismonthfp = OrderDetail.objects.filter(creater__user__is_superuser=True, order__custome=user,
                                             createtime__month=now.month).exclude(status=12).count()  # 查看本月分配的数据
    thismonth = OrderDetail.objects.filter(creater=user).filter(createtime__month=now.month).count()  # 本月累计跟进人次
    thismonthrl = OrderDetail.objects.filter(createtime__month=now.month).filter(status=2, creater=user).count()  # 本月认领
    v1 = OrderDetail.objects.filter(status=6, createtime__month=now.month).filter(creater=user).count()  # 本月已安排治疗
    v2 = OrderDetail.objects.filter(status=11, createtime__month=now.month).filter(creater=user).count()  # 延后治疗
    v3 = OrderDetail.objects.filter(status=13, createtime__month=now.month).filter(creater=user).count()  # 转院的
    v4 = OrderDetail.objects.filter(status=12, createtime__month=now.month).filter(creater=user).count()  # 暂停的
    # 查看全部
    thismonthall = OrderDetail.objects.filter(creater=user).count()  # 全部累计跟进人次
    thismonthfpall = OrderDetail.objects.filter(creater__user__is_superuser=True, order__custome=user, ).exclude(
        status=12).count()  # 查看全部分配的数据
    thismonthrlall = OrderDetail.objects.filter(status=2, creater=user).count()  # 全部认领
    v1all = OrderDetail.objects.filter(status=6, creater=user).count()  # 全部已安排治疗
    v2all = OrderDetail.objects.filter(status=11, creater=user).count()  # 全部延后治疗
    v3all = OrderDetail.objects.filter(status=13, creater=user).count()  # 全部转院的
    v4all = OrderDetail.objects.filter(status=12, creater=user).count()  # 全部暂停的
    return render(request, 'formManage.html',
                  {"pageindex": 3, "menu": MENUS_CALLER, 'thismonth': thismonth, 'thismonthfp': thismonthfp,
                   'thismonthrl': thismonthrl, 'v1': v1, 'v2': v2, 'v3': v3, 'v4': v4, 'thismonthall': thismonthall,
                   'thismonthfpall': thismonthfpall, 'thismonthrlall': thismonthrlall, 'v1all': v1all, 'v2all': v2all,
                   'v3all': v3all, 'v4all': v4all})


@login_required(login_url="/login/")
def index(request):
    # print "拿到的是什么",request.user.is_active
    # all_datas = YourModel.objects.filter(time__year=now_time.year) #查询某年的
    # all_datas = YourModel.objects.filter(time__month=now_time.month)#查询当前月份的
    user = ZJUser.objects.get(user=request.user)

    now = datetime.datetime.now()

    thismonth = OrderDetail.objects.filter(creater=user).filter(createtime__month=now.month).count()  # 本月跟进工单

    thismonthfp = OrderDetail.objects.filter(creater__user__is_superuser=True).filter(status=6).filter(
        createtime__month=now.month).count()  # 本月分配
    thismonthrl = OrderDetail.objects.filter(createtime__month=now.month).filter(status=2, creater=user).count()

    v1 = OrderDetail.objects.filter(status=6).filter(creater=user).count()  # 已安排治疗
    v2 = OrderDetail.objects.filter(status=11).filter(creater=user).count()
    v3 = OrderDetail.objects.filter(status=13).filter(creater=user).count()
    v4 = OrderDetail.objects.filter(status=12).filter(creater=user).count()

    todaywork = Order.objects.filter(nextcalldate__lte=now, custome=user)[:5]  # 今日任务

    renling = Order.objects.filter(status=1, custome__isnull=True)
    arr = getNotify(request.user)
    # identity=manag.usertype #身份(1,'客服')(2,'销售'),(3,'管理员')

    return render(request, "index.html",
                  {"user": user, "thismonth": thismonth, "thismonthfp": thismonthfp, "thismonthrl": thismonthrl,
                   "v1": v1, "v2": v2, "v3": v3, "v4": v4, "todaywork": todaywork, "notify": arr, "renling": renling,
                   "pageindex": 0, "menu": MENUS_CALLER})


def notify(request):
    arr = getNotify()

    return JsonResutResponse({"data": arr})


def getNotify(user):
    now = datetime.datetime.now()
    user = ZJUser.objects.get(user=user)
    yestoday = now - timedelta(days=1)
    notify1 = Order.objects.filter(Order__creater__user__is_superuser=True).filter(Order__is_operation=False,
                                                                                   custome=user)  # 管理员分配
    notify2 = Order.objects.filter(Order__creater__usertype=2).filter(Order__is_operation=False, custome=user)  # 有备注
    notify3 = Order.objects.filter(nextcalldate__lte=yestoday.date(), custome=user).exclude(status=12)  # 逾期了

    arr = []
    for n in notify1:
        dic = {}
        data = {
            'id': n.id,
            'name': n.name,
            'hosp': n.wanthospital,
            'time': n.wantTime,
            'type': 1
        }
        if checkdicinlist(arr, n.id):
            arr.append(data)
    for n in notify2:
        dic = {}
        data = {
            'id': n.id,
            'name': n.name,
            'hosp': n.wanthospital,
            'time': n.wantTime,
            'type': 2
        }
        if checkdicinlist(arr, n.id):
            arr.append(data)
    for n in notify3:
        dic = {}
        data = {
            'id': n.id,
            'name': n.name,
            'hosp': n.wanthospital,
            'time': n.wantTime,
            'type': 3,
            'yuqu': (datetime.datetime.now().date() - n.nextcalldate).days
        }
        if checkdicinlist(arr, n.id):
            arr.append(data)
    t = template.loader.get_template("control/notify.html")
    c = template.Context({'notify': arr[:4]})
    return t.render(c)


def todaywork(request):
    user = ZJUser.objects.get(user=request.user)

    now = datetime.datetime.now()
    yestoday = now - timedelta(days=1)

    todaywork = Order.objects.filter(nextcalldate__lte=now, custome=user)[0:5]  # 今日任务
    t = template.loader.get_template("control/today.html")
    c = template.Context({'todaywork': todaywork})
    return JsonResutResponse({"result": 1, "data": t.render(c)})


def checkdicinlist(arr, sid):
    for a in arr:
        if a['id'] == sid:
            return False
    return True


@login_required(login_url="/login/")
def renling(request):
    sid = request.GET.get("id")
    order = Order.objects.filter(pk=sid).first()
    hosp = Hospital.objects.all()
    area = Area.objects.all()
    print order.pation.all()
    return render(request, "hzrlpop.html", {"order": order, "hosp": hosp, "area": area, 'imgs': order.pation.all()})


@login_required(login_url="/login/")
def renlingAction(request):
    sid = request.POST.get("sid")
    order = Order.objects.get(pk=sid)
    if order.custome:
        return HttpResponse("{\"result\":-1,\"msg\":\"已经被认领\"}")
    customer = ZJUser.objects.get(user=request.user)
    order.custome = customer
    order.nextcalldate = datetime.datetime.now().date()
    order.status = 2
    order.save()
    OrderDetail(order=order, creater=customer, createtime=datetime.datetime.now(), status=2, remark="认领").save()
    return JsonResutResponse({"result": 1, "msg": "认领成功"})


def pationsview(request):
    type = request.GET.get("type", False)
    user = request.user
    cus = ZJUser.objects.filter(user=user)
    orders = Order.objects.filter(custome=cus).order_by("-wantTime")
    if type:
        now = datetime.datetime.now()
        orders.filter(nextcalldate__lte=now)
    order = orders[:10]

    return render(request, "patientManage.html",
                  {"pageindex": 1, "menu": MENUS_CALLER, "all": orders.count(), "order": order,
                   "type": type if type else ""})


@login_required(login_url="/login/")
def pations(request):
    user = request.user
    cus = ZJUser.objects.filter(user=user)
    orders = Order.objects.filter(custome=cus).order_by("-wantTime")
    return JsonResutResponse({"result": 1, "list": list(orders)})


@login_required(login_url="/login/")
def remind(request):
    user = ZJUser.objects.get(user=request.user)
    now = datetime.datetime.now()
    yestoday = now - timedelta(days=1)
    orders = Order.objects.filter(custome=user, nextcalldate__lte=yestoday.date(), nextcalldate__isnull=False).exclude(
        status=12).order_by('-createtime')
    remin = Order.objects.filter(custome=user).filter(Order__creater__usertype=2).filter(
        Order__is_operation=False).order_by('-createtime')  # 所有备忘
    admin = Order.objects.filter(custome=user).filter(Order__creater__user__is_superuser=True).filter(
        Order__is_operation=False).order_by('-createtime')  # 查看分配
    if orders:
        lister = RemindSystem(orders[:5])  # 这是逾期的
    else:
        lister = []
    if remin:
        notes = ViewCheat(remin[:3])  # 这里是备忘
    else:
        notes = []
    if admin:
        admins = AdminDis(admin[:3])  # 这里是管理员分配的
    else:
        admins = []
    return render(request, "remindManage.html",
                  {'ret': 0, 'msg': 'success', 'lister': lister, 'notes': notes, 'admin': admins, "pageindex": 2,
                   "menu": MENUS_CALLER})


def account(request):
    return render(request, "accountManage.html", {"pageindex": 4, "menu": MENUS_CALLER})


def addpation(request):
    hosp = Hospital.objects.all()
    area = Area.objects.all()

    return render(request, "addpeople.html", {"hosp": hosp, "area": area})


@login_required(login_url="/login/")
def orderdetail(request):
    user = ZJUser.objects.get(user=request.user)
    id = request.GET.get('id')  # 患者订单的id
    order = Order.objects.filter(id=id).first()  # 患者订单
    imgs = IllnessImage.objects.filter(patient=order).values("image")  # 患者上传的图片

    follows = OrderDetail.objects.filter(order=order).order_by('-createtime')  # 对订单的所有操作
    if order.custome == user:
        follows.filter(is_operation=False).update(is_operation=True)
    hosp = Hospital.objects.all()
    area = Area.objects.all()

    return render(request, "OrderDetail.html",
                  {"order": order, "imgs": imgs, "follows": follows, "iscreater": order.custome == user, "hosp": hosp,
                   "area": area})


# 上传图片
def uploader(request):
    img = request.FILES.get('file')
    img_url = Compression(img)
    return HttpResponse(simplejson.dumps({"result": 0, "imgurl": img_url}))


@login_required(login_url="/login/")
def OrderSubmit(request):
    userinfo = request.POST['userinfo']
    photo = request.POST['photo']
    cid = request.user
    zuser = ZJUser.objects.filter(user=cid).first()
    print userinfo, photo
    user = json.loads(userinfo)  # 用户
    photos = json.loads(photo)  # 图片
    item = {}
    for k in user:
        if k == 'name':
            name = user[k]
            item[k] = user[k]
        elif k == 'wanthospital':
            hosp = Hospital.objects.filter(id=user[k]).first()
            item[k] = hosp
        elif k == 'phone':
            phone = user[k]
            item[k] = user[k]
        elif k == 'area':
            area = Area.objects.filter(id=user[k]).first()
            item[k] = area
        else:
            item[k] = user[k]
    order = Order.objects.filter(name=name, phone=phone)
    if order:
        return JsonResutResponse({'ret': 1, 'msg': '已有预约正在进行中'})
    else:
        orders = Order.objects.all()
        n = len(orders) + 1
        s = "NO.%04d" % n
        item['serial'] = s
        item['custome_id'] = zuser.id
        item["status"] = 2
        order = Order.objects.create(**item)
    for photo in photos:
        IllnessImage.objects.create(image=photo, patient=order)
    return JsonResutResponse({'ret': 0, 'msg': 'success'})


@login_required(login_url="/login/")
def OrderUpdte(request):
    userinfo = request.POST['userinfo']
    photo = request.POST['photo']
    folow = request.POST['folow']
    cid = request.user
    zuser = ZJUser.objects.filter(user=cid).first()
    user = json.loads(userinfo)  # 用户
    photos = json.loads(photo)  # 图片
    folows = json.loads(folow)
    item = {}
    for k in user:
        if k == 'name':
            name = user[k]
            item[k] = user[k]
        elif k == 'wanthospital':
            hosp = Hospital.objects.filter(id=user[k]).first()
            item[k] = hosp
        elif k == 'phone':
            phone = user[k]
            item[k] = user[k]
        elif k == 'area':
            area = Area.objects.filter(id=user[k]).first()
            item[k] = area
        elif k == 'oid':
            pass

        else:
            item[k] = user[k]
    order = Order.objects.filter(id=user['oid'])
    u = order.update(**item)
    IllnessImage.objects.filter(patient=order.first()).delete()
    for photo in photos:
        IllnessImage.objects.create(image=photo, patient=order.first())
    folowitem = {}
    for f in folows:
        folowitem[f] = folows[f]
    folowitem['order_id'] = user['oid']
    folowitem['creater_id'] = zuser.id
    desc = u'将%s进行了%s的操作' % (order.first().name, getStatusName(folows['status']))
    folowitem['remark'] = desc
    OrderDetail.objects.create(**folowitem)
    order = order.first()
    if order.status == 3:  # 确认去就诊
        try:
            CeleTexting(user['oid'], 2)  # 发短信
            CreateSMS(order)  # 定时发消息
            CreateCelery(order)  # 定时发模板消息
        except:
            pass
        if order.openid:
            ModelMsg(user['oid'], 1, 2)  # 发模板消息
        if order.wanthospital.sales.openid:
            ModelMsg(user['oid'], 2, 2)  # 给销售发模板消息
    return JsonResutResponse({'ret': 0, 'msg': 'success'})


# def IntegralChange(touser, template_id, url, first, value1, value2, value3):
#   sJson = {'touser': touser,
#            'template_id': template_id,
#            "url": url,
#            'data': {
#              'first': {
#                "value": first  # first_value % realname
#              },
#              'keyword1': {
#                "value": value1
#              },
#              'keyword2': {
#                "value": value2
#              },
#              'keyword3': {
#                "value": value3
#              },
#              'remark': {"value": "请点击“详情”了解具体信息"}
#            },
#            }
#   try:
#     url = 'http://wx.yuemia.com/wechat/sendtemp.ashx'
#     parm = {"wx":'xinghui', "data": json.dumps(sJson)}
#     r = requests.post(url, parm)
#     print 'temp re:',r.content
#     if (eval(r.content)['errcode'] != 0):
#       print eval(r.content)
#       return False
#   except Exception, e:
#
#     print 'errorL',e.message
#     return e.message
#   return True

def getStatusName(statusvalue):
    return CHIOCE[int(statusvalue) - 1][1]


def overdue(request):
    user = ZJUser.objects.get(user=request.user)
    now = datetime.datetime.now()
    yestoday = now - timedelta(days=1)
    orders = Order.objects.filter(custome=user, nextcalldate__lte=yestoday.date(), nextcalldate__isnull=False).exclude(
        status=12).order_by(
        '-createtime')[:10]
    if len(orders) > 0:
        lister = RemindSystem(orders)  # 这是逾期的
    else:
        lister = []
    return render(request, "overdue.html", {"pageindex": 2, "menu": MENUS_CALLER, "lister": lister})


def salercommit(request):
    user = ZJUser.objects.get(user=request.user)
    remin = Order.objects.filter(custome=user).filter(Order__creater__usertype=2).filter(
        Order__is_operation=False).order_by('-createtime')  # 所有备忘
    return render(request, "salercommitlist.html", {"pageindex": 2, "menu": MENUS_CALLER, "order": remin})


def adminfenpei(request):
    user = ZJUser.objects.get(user=request.user)
    admin = Order.objects.filter(custome=user).filter(Order__creater__user__is_superuser=True).filter(
        Order__is_operation=False).order_by('-createtime')  # 查看分配

    return render(request, "fenpeilist.html", {"pageindex": 2, "menu": MENUS_CALLER, "order": admin})


def staffaddnew(request):
    area = Area.objects.all()
    return render(request, "admin/addnewStaff.html", {"area": area})


@login_required(login_url="/login/")
def yuqi(request):
    user = ZJUser.objects.get(user=request.user)
    now = datetime.datetime.now()
    yestoday = now - timedelta(days=1)
    orders = Order.objects.filter(custome=user, nextcalldate__lte=yestoday.date(), nextcalldate__isnull=False).exclude(
        status=12).order_by(
        '-createtime')[:5]
    if len(orders) > 0:
        lister = RemindSystem(orders)  # 这是逾期的
    else:
        lister = []
    t = template.loader.get_template("control/yuqiitem.html")
    c = template.Context({'lister': lister})
    return JsonResutResponse({"data": t.render(c)})
