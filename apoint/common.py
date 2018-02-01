#coding:utf-8
from models import *
from django.http import HttpResponse
import simplejson
from PIL import Image as image
import time
import os
from django.core.paginator import Paginator
import datetime
def JsonResutResponse(result):
  return HttpResponse(simplejson.dumps(result))



def Console():
    user=u'用户'
    #all_datas = YourModel.objects.filter(time__year=now_time.year) #查询某年的
    #all_datas = YourModel.objects.filter(time__month=now_time.month)#查询当前月份的
    pass

#压缩图片
def Compression(img):
    im=image.open(img)
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
    file_url = 'static/upload/%s.%s'%(timestamp,pos)
    # im.save(file_url,quality=50)
    im.save(file_url)
    return '/'+file_url

#分页
def Paging(data,page):
  paginator = Paginator(data, 10)
  if paginator.num_pages > int(page):
      result = False
      contacts = paginator.page(page)
  elif paginator.num_pages == int(page):
      result = True
      contacts = paginator.page(page)
  else:
    result=True
    contacts=None
  return result,contacts


#查看患者详情的方法
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
    if follows:
        for follow in follows:
            date = {
                'name': follow.creater.name,  # 客服姓名
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
        'number':order.number,#治疗次数
        'description': order.description,  # 描述
        'photo': lister,  # 照片
    }
    return date,record

#客服查看系统提醒(逾期)
def RemindSystem(orders):
    lister = []
    now = datetime.datetime.now()  # 当前时间
    if orders:
        for order in orders:
            nextcalldate = order.nextcalldate.strftime('%Y-%m-%d')
            filsday = datetime.datetime.strptime(nextcalldate, '%Y-%m-%d')  # 数据库的时间
            time_diff = (now - filsday).days  # 当前时间和下次电话时间的差
            if time_diff > 0:
                data = {
                    'id': order.id,
                    'name': order.name,
                    'wanthospital': order.wanthospital.name,  # 医院名称
                    'wantTime': order.wantTime.strftime('%Y-%m-%d  %H:%M'),  # 预约时间
                    'status': order.get_status_display(),  # 患者状态
                    'nextcalldate': nextcalldate,  # 计划时间
                    'day': time_diff,  # 逾期天数
                    'sales': order.wanthospital.sales.name,  # 负责销售
                }
                lister.append(data)
            else:
                pass
    else:
        pass
    return lister

#客服查看系统提醒(提交的备忘)
def ViewCheat(orders):
    notes=[]
    if orders:
        for order in orders:
            data={
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
#查看管理员分配的
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
