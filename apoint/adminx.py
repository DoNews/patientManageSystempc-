# encoding=utf8
import xadmin
from models import *
#class ZJUseradmin(object):
class OrderDetailDisplay(object):
    search_fields=['creater',]

xadmin.site.register(ZJUser)
xadmin.site.register(SalesUser)
xadmin.site.register(Order) #患者订单
xadmin.site.register(Area)#省
xadmin.site.register(Hospital)#医院
xadmin.site.register(OrderDetail,OrderDetailDisplay)#客服描述