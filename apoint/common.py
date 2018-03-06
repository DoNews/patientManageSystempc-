# coding:utf-8
from models import *
from django.http import HttpResponse
import simplejson
from PIL import Image as image
import time
from django.utils import timezone
import os
from django.core.paginator import Paginator
from task import *
import datetime
from django import template


def JsonResutResponse(result):
    return HttpResponse(simplejson.dumps(result))


def Console():
    user = u'用户'
    # all_datas = YourModel.objects.filter(time__year=now_time.year) #查询某年的
    # all_datas = YourModel.objects.filter(time__month=now_time.month)#查询当前月份的
    pass


# 压缩图片
def Compression(img):
    im = image.open(img)
    # width=im.size[0]
    # height=im.size[1]
    # ratio=width/height
    # if width>1080:
    #     width=1080
    # width=int(width)
    # height=int(width*ratio)
    # im.resize((width,height), image.ANTIALIAS)
    timestamp = str(int(time.time()))
    pos = str(img).split('.')[-1]
    file_url = 'static/upload/%s.%s' % (timestamp, pos)
    # im.save(file_url,quality=50)
    im.save(file_url)
    return '/' + file_url


# 分页
def Paging(data, page):
    paginator = Paginator(data, 10)
    if paginator.num_pages > int(page):
        result = False
        contacts = paginator.page(page)
    elif paginator.num_pages == int(page):
        result = True
        contacts = paginator.page(page)
    else:
        result = True
        contacts = None
    return result, contacts


# 查看患者详情的方法
def Detail(order):
    imgs = IllnessImage.objects.filter(patient=order)  # 患者上传的图片
    follows = OrderDetail.objects.filter(order=order)  # 对订单的所有操作
    lister = []
    record = []
    if imgs:
        for img in imgs:
            lister.append(img.image)
    else:
        pass
    if len(follows)>3:
        is_end=False
    else:
        is_end=True
    if follows:
        followser=follows[:3]
        for follow in followser:
            date = {
                'name': follow.creater.name if follow.creater  else '',  # 客服姓名
                'remark': follow.remark,  # 描述
                'time': follow.createtime.strftime('%Y-%m-%d %H:%M')
            }
            record.append(date)
    else:
        pass
    date = {
        'name': order.name,  # 患者名称
        'sex': order.sex,  # 性别
        'serial': order.serial,  # 编号
        'birthday': order.birthday.strftime('%Y-%m-%d'),  # 生日
        'phone': order.phone,  # 手机
        'wantTime': order.wantTime.strftime('%Y-%m-%d'),  # 期望预约时间
        'wanthospital': order.wanthospital.name,  # 预约医院
        'area': order.area.name,  # 省
        'number': order.number,  # 治疗次数
        'description': order.description,  # 描述
        'photo': lister,  # 照片
    }
    return date, record ,is_end


# 客服查看系统提醒(逾期)
def RemindSystem(orders):
    lister = []
    now = datetime.datetime.now().date()  # 当前时间
    if orders:
        for order in orders:
            print 't:', order.nextcalldate, order.id
            time_diff = (now - order.nextcalldate).days  # 当前时间和下次电话时间的差
            if time_diff > 0:
                data = {
                    'id': order.id,
                    'name': order.name,
                    'wanthospital': order.wanthospital.name,  # 医院名称
                    'wantTime': order.wantTime.strftime('%Y-%m-%d  %H:%M'),  # 预约时间
                    'status': order.get_status_display(),  # 患者状态
                    'nextcalldate': order.nextcalldate,  # 计划时间
                    'day': time_diff,  # 逾期天数
                    'sales': order.wanthospital.sales.name if order.wanthospital.sales else '无',  # 负责销售
                }
                lister.append(data)
            else:
                pass
    else:
        pass
    return lister


# 客服查看系统提醒(提交的备忘)
def ViewCheat(orders):
    notes = []
    if orders:
        for order in orders:
            data = {
                'id': order.id,  # 订单id
                'name': order.name,  # 姓名
                'wanthospital': order.wanthospital.name,  # 医院名称
                'wantTime': order.wantTime.strftime('%Y-%m-%d  %H:%M'),
                'sales': order.wanthospital.sales.name,  # 负责销售
            }
            notes.append(data)
    else:
        pass
    return notes


# 查看管理员分配的
def AdminDis(orders):
    admins = []
    if orders:
        for order in orders:
            data = {
                'id': order.id,  # 订单id
                'name': order.name,  # 姓名
                'wanthospital': order.wanthospital.name,  # 医院名称
                'wantTime': order.wantTime.strftime('%Y-%m-%d  %H:%M'),  # 预约时间
            }
            admins.append(data)
    else:
        pass
    return admins


# 这是定时用的
def CreateMiss(id, name, msgtype, started_time, equipment):  # equipment 1是手机短信定时，2是微信模板定时
    task_args = {'SentWhoId': id, 'MsgType': msgtype}
    out_time = started_time + settings.OUTDATE_ONEDAY  # 删除时间
    if equipment == 1:
        if msgtype == 1:  # 预约前三天
            name = "%s%s%s" % (name, id, u'手机短信前三天')
            end_time = started_time - settings.OUTDATE_PERIOD
        else:  # 预约当天8点
            name = "%s%s%s" % (name, id, u'手机短信当天八点')
            end_time = started_time + settings.OUTDATE_HOURS  # 当天加上8小时
    else:
        # if msgtype == 2:  # 预约前三天
        #     name = "%s%s%s" % (name, id, u'微信模板前三天') ##消失了
        #     end_time = started_time - settings.OUTDATE_PERIOD
        if msgtype == 1:
            name = "%s%s%s" % (name, id, u'微信模板前一天')
            end_time = started_time - settings.OUTDATE_ONEDAY
        else:  # 预约当天8点
            name = "%s%s%s" % (name, id, u'微信模板当天八点')
            end_time = started_time + settings.OUTDATE_HOURS  # 当天加上8小时
    crontab_time = {
        'month_of_year': end_time.month,  # 月份
        'day_of_month': end_time.day,  # 日期
        'hour': end_time.hour,  # 小时 c
        'minute': end_time.minute,  # 分钟
    }
    if equipment == 1:
        create_task(name, 'apoint.tasks.CeleTexting', task_args, crontab_time, out_time)
    else:
        create_task(name, 'apoint.tasks.TimingModel', task_args, crontab_time, out_time)


# 这是为了定时发模板消息用的
def CreateCelery(order):  #
    new = timezone.now()
    if order.wantTime - settings.OUTDATE_ONEDAY > new:
        a = 2
    elif order.wantTime - settings.OUTDATE_HOURS > new:
        a = 1
    else:
        a = 0
    for b in range(a):  # 0是8小时，1是一天，2是3天
        CreateMiss(order.id, order.name, b, order.wantTime, 2)


# 这是定时发短信
def CreateSMS(order):
    new = timezone.now()
    if order.wantTime - settings.OUTDATE_PERIOD > new:
        a = 2
    else:
        a = 1
    for b in range(a):  # 1是当天8点，2是3天
        CreateMiss(order.id, order.name, b, order.wantTime, 1)


def trenderc(templates, lister):
    t = template.loader.get_template(templates)
    c = template.Context({'lister': lister})
    return t.render(c)
