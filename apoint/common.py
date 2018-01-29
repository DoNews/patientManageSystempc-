#coding:utf-8
from models import *
from django.http import HttpResponse
import simplejson
from PIL import Image as image
import time
import os

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