#coding: utf8
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,UserManager,User
from django.db.models.signals import post_save



class Area(models.Model):
    name= models.CharField(u'省',null=True,blank=True,max_length=255)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name='省'
        verbose_name_plural='省'

#后台操作身份
class ZJUser(models.Model):
    USER_TYPE=(
        (1,'客服'),
        (2,'销售'),
        (3,'管理员')
    )
    user = models.OneToOneField(User,null=True,blank=True)
    name = models.CharField('姓名', max_length=20)
    usertype=models.IntegerField("用户类型",choices=USER_TYPE,default=1)
    phone=models.CharField('手机号',max_length=50)
    def __unicode__(self):
        return self.name

#销售认证
class SalesUser(ZJUser):
    openid = models.CharField("openid", max_length=100, blank=True,null=True)
    email=models.CharField('邮箱',max_length=50)
    is_cert=models.BooleanField('是否认证',default=False)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name='员工'
        verbose_name_plural='员工'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = ZJUser.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
#医院，
class Hospital(models.Model):
    name = models.CharField(u'医院名称',null=True,blank=True,max_length=255)
    province=models.ForeignKey(Area,verbose_name='对应省',blank=True,null=True)
    address=models.CharField('具体地址',max_length=100,null=True,blank=True)
    manager=models.CharField('大区经理',max_length=20,null=True,blank=True)
    sales=models.ForeignKey(SalesUser,verbose_name='对应的销售',null=True,blank=True)
    link=models.CharField('图文链接',max_length=100,null=True,blank=True)
    confirm=models.CharField('确认就诊短信',max_length=100,null=True,blank=True)
    three=models.CharField('前三天短信',max_length=100,null=True,blank=True)
    inday=models.CharField('当天提醒短信',max_length=100,null=True,blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name='医院'
        verbose_name_plural='医院'
#患者订单
CHIOCE=((1,'未认领'),
        (2,'已认领未确认'),
        (3,'确认去就诊'),
        (4,'确认不就诊'),
        (5,'延期预约'),
        (6,'已安排治疗'),
        (7,'完成首次随访'),
        (8,'完成15日随访'),
        (9,'完成30日随访'),
        (10,'完成45日随访'),
        (11,'延后治疗'),
        (12,'暂停跟进'),
        (13,'转院'),
        (14,'确认未到诊'))



class Order(models.Model):
    openid = models.CharField('openid', max_length=100, blank=True, null=True)
    name = models.CharField(u'患者姓名',null=True,blank=True,max_length=255)
    birthday = models.DateTimeField(u'出生日期',null=True,blank=True)
    sex = models.CharField(u'性别',null=True,blank=True,max_length=10)
    phone = models.CharField(u'手机',null=True,blank=True,max_length=50)
    area = models.ForeignKey(Area,verbose_name="省",null=True,blank=True)
    wantTime = models.DateTimeField(u'就诊时间',null=True)
    number=models.IntegerField(u'治疗次数',default=0)
    wanthospital=models.ForeignKey(Hospital,verbose_name="医院名称")
    description =models.CharField(u'病情描述',null=True,blank=True,max_length=1000)
    createtime=models.DateTimeField(u'提交时间',auto_now_add=True)
    nextcalldate =models.DateField("下次电话时间",null=True)
    status =models.IntegerField(u'当前状态',choices=CHIOCE,default=1)
    custome=models.ForeignKey(ZJUser,related_name='user_custom',verbose_name='所属客服',null=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name='患者订单'
        verbose_name_plural='患者订单'

#患者订单图
class IllnessImage(models.Model):
    image = models.CharField(u'病情图片链接',max_length=200)
    patient = models.ForeignKey(Order,verbose_name="上传人")
# Create your models here.


class OrderDetail(models.Model):
    order = models.ForeignKey(Order,verbose_name="所属预约")
    creater = models.ForeignKey(ZJUser,verbose_name="操作人",related_name="Order")
    createtime=models.DateTimeField("操作时间",auto_now_add=True)
    status = models.IntegerField("状态",choices=CHIOCE,default=0)
    remark =models.CharField("描述",max_length=1000,null=True)
    is_operation=models.BooleanField(u'是否操作',default=False)
    nextcalldate = models.DateField("下次电话时间",null=True)
    def __unicode__(self):
        return self.order.name
    class Meta:
        verbose_name='确认与备忘'
        verbose_name_plural='确认与备忘'


