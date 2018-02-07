# # coding:utf-8
# from djcelery import models as celery_models
# from django.utils import timezone
# from celery import task
# from Apointment import settings
# from models import *
# import logging
# import json
# import requests
# import threading
# from time import ctime,sleep
#
# @task
# def TimingModel(SentWhoId,MsgType):
#     order = Order.objects.get(id=SentWhoId) #根据id 找到订单的id
#     if MsgType == 1:
#         conten = u"尊敬的%s: 您的如下就诊预约就要到了，我们特别提醒您按时到院就诊"%order.name
#     else:
#         conten = u"尊敬的%s: 您今天安排了如下就诊预约，我们特别提醒您按时到院就诊"
#     detail_url = settings.SiteHost + "/static/dist/#/live/%s"%SentWhoId
#     first = conten
#     template_id =settings.PATIENTS_MODE  #模板id
#     touser = order.openid  # 发送给谁
#     value1 = order.wanthospital.name  # 医院名称
#     value2 = order.wantTime.strftime('%Y-%m-%d %H:%M')  # 活动日期
#     value3 = order.get_status_display()
#     t1 = threading.Thread(target=ModelNews, args=(touser, template_id, detail_url, first, value1, value2, value3))
#     t1.start()
#     sleep(3)
#
#
# #发送给患者和销售模板消息
# #msgtype 为1的时候是给患者发 为2 是给销售发，semtwhoId 是订单详情,Sendtype为（1,提交成功),(2,确认),（3,延时预约）
# def ModelMsg(SentWhoId,msgtype,Sendtype):
#     if msgtype==1: #为一的时候是给患者发
#         order=Order.objects.get(id=SentWhoId) #找到患者的订单
#         detail_url = order.wanthospital.link
#         if Sendtype==1:
#             first = "尊敬的%s:您的如下就诊预约已经提交，我们会尽快和您电话确认相关信息"%order.name
#         elif Sendtype==2:
#             first="尊敬的%s:您的如下就诊预约已经确认，我们特别提醒您按时到院就诊"%order.name
#         else:
#             first="尊敬的%s:您的如下就诊预约申请已经延期，感谢您的支持与配合"%order.name
#         template_id = settings.PATIENTS_MODE #模板ID
#         touser = order.openid #发送给谁
#         value1 = order.wanthospital.name  # 医院名称
#         value2 = order.wantTime.strftime('%Y-%m-%d %H:%M')  # 就诊日期
#         value3 = order.get_status_display()
#         ModelNews(touser, template_id, detail_url, first, value1, value2, value3)
#     else:
#         order = Order.objects.get(id=SentWhoId)  # 找到患者的订单
#         detail_url = settings.SiteHost + "/static/MobileClient/Saler/PatientInfo.html?id=%s"%SentWhoId
#         first = "尊敬的%s:您所负责的医院有新患者确认了预约"%order.wanthospital.sales.name
#         template_id = settings.SALES_MODE  # 模板ID
#         touser = order.wanthospital.sales.openid  # 发送给谁
#         value1 = order.name,  # 预约患者
#         value2 = order.wanthospital.name  # 医院名称
#         value3 = order.wantTime.strftime('%Y-%m-%d %H:%M')  # 就诊日期
#         value4 = order.get_status_display()
#         IntegralChange(touser, template_id, detail_url, first, value1, value2, value3, value4,)
#
# # 发送模板消息
# def ModelNews(touser, template_id, url, first, value1, value2, value3):
#   sJson = {'touser': touser,
#            'template_id': template_id,
#            "url": url,
#            'data': {
#              'first': {
#                "value": first # first_value % realname
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
#              'remark': {"value": '点击详情查看情况'}
#            },
#            }
#   try:
#     url = 'http://wx.yuemia.com/wechat/sendtemp.ashx'
#     parm ={"wx":settings.WEIXIN,"data":json.dumps(sJson)}
#     r=requests.post(url, parm)
#     logger = logging.getLogger("tasks")
#     logger.error(r.content, exc_info=True)
#     if (eval(r.content)['errcode'] != 0):
#       print eval(r.content)
#       return False
#   except Exception, e:
#     logger = logging.getLogger("tasks")
#     logger.error(e, exc_info=True)
#     return e.message
#   return True
#
# # 销售的模板消息
# def IntegralChange(touser, template_id, url, first, value1, value2, value3, value4,):
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
#              'keyword4': {
#                "value": value4
#              },
#              'remark': {"value": "请点击“详情”了解具体患者信息并进行线下的跟进吧"}
#            },
#            }
#   try:
#     url = 'http://wx.yuemia.com/wechat/sendtemp.ashx'
#     parm = {"wx":settings.WEIXIN, "data": json.dumps(sJson)}
#     r = requests.post(url, parm)
#     if (eval(r.content)['errcode'] != 0):
#       print eval(r.content)
#       return False
#   except Exception, e:
#     logger = logging.getLogger("tasks")
#     logger.error(e, exc_info=True)
#     return e.message
#   return True
#
#
#
#
# #定时发短信,或发短信
# @task
# def CeleTexting(SentWhoId,MsgType):
#     order=Order.objects.get(id=SentWhoId)
#     if MsgType == 1:
#         conten = order.wanthospital.three
#     else:
#         conten = order.wanthospital.inday
#     http = "http://222.73.117.158:80/msg/HttpBatchSendSM"
#     r = requests.post(http, {"account": "muai37", "pswd": "Muai888123", "mobile": "%s" % order.phone, "msg": "%s" %conten,"needstatus": "false"})
#     logger = logging.getLogger('csrfcode')
#     logger.info(r)
#     logging.error(r.content)
#
# @task
# # 创建任务，创建定时任务，
# def create_task(name, task, task_args, crontab_time,out_time):
#   try:
#     '''
#     name # 任务名字
#     task # 执行的任务 "myapp.tasks.add"
#     task_args # 任务参数 {"x":1, "Y":1}
#
#     crontab_time # 定时任务时间 格式：
#     {
#         'month_of_year': 9 # 月份
#         'day_of_month': 5 # 日期
#         'hour': 01 # 小时
#         'minute':05 # 分钟
#     }
#     '''
#     # task任务， created是否定时创建
#     task, created = celery_models.PeriodicTask.objects.get_or_create(name=name, task=task)
#     crontab = celery_models.CrontabSchedule.objects.filter(**crontab_time).first()
#     if crontab is None:
#       # 如果没有就创建，有的话就继续复用之前的crontab
#       crontab = celery_models.CrontabSchedule.objects.create(**crontab_time)
#     task.crontab = crontab  # 设置crontab
#     task.enabled = True  # 开启task
#     task.kwargs = json.dumps(task_args)  # 传入task参数
#     task.expires = out_time # 设置任务过期时间为现在时间的11天以后
#     task.save()
#   except Exception, e:
#     logger = logging.getLogger("tasks")
#     logger.error(e, exc_info=True)
#   return True
#
# @task
# def delete():
#     '''
#     删除任务
#     从models中过滤出过期时间小于现在的时间然后删除
#     '''
#     return celery_models.PeriodicTask.objects.filter(
#                             expires__lt=timezone.now()).delete()