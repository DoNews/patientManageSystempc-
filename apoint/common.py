#coding:utf-8
from models import *
from django.http import HttpResponse
import simplejson

def JsonResutResponse(result):
  return HttpResponse(simplejson.dumps(result))



def Console():
    user=u'用户'
    #all_datas = YourModel.objects.filter(time__year=now_time.year) #查询某年的
    #all_datas = YourModel.objects.filter(time__month=now_time.month)#查询当前月份的
    pass