# encoding=utf8
import xadmin
from models import *
#class ZJUseradmin(object):
xadmin.site.register(ZJUser)
xadmin.site.register(SalesUser)
xadmin.site.register(Order) #患者订单
xadmin.site.register(Area)#省
xadmin.site.register(Hospital)#医院
xadmin.site.register(OrderDetail)#客服描述