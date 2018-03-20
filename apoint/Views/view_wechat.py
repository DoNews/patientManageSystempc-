from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from apoint.Views.view_wx import *
def checkUser(request):
    openid = request.GET.get("openid")
    o = Order.objects.filter(openid=openid)
    if len(o)>0:
        return HttpResponseRedirect("http://yuyue.tianshizhiwen.org/static/MobileClient/Patient/AppiontmentSuccess.html")
    else:
        return HttpResponseRedirect("http://yuyue.tianshizhiwen.org/static/MobileClient/Patient/Appiontment.html?openid="+openid)

def order(request):
    agent = request.META.get('HTTP_USER_AGENT')
    if agent.lower().find("micromessenger")>-1:
        return HttpResponseRedirect("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxcf86e59e9c228363&redirect_uri=http%3A%2F%2Fwx.yuemia.com%2Fwechat%2Fopenid.ashx%3Fwx%3Dfindangel%26type%3D1%26Url%3Dhttp%253A%252F%252Fyuyue.tianshizhiwen.org%252FcheckUser&response_type=code&scope=snsapi_base&state=O#wechat_redirect")
    else:
        return HttpResponseRedirect("http://yuyue.tianshizhiwen.org/static/MobileClient/Patient/Appiontment.html")

def reg(req):

    return HttpResponseRedirect("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxcf86e59e9c228363&redirect_uri=http%3A%2F%2Fwx.yuemia.com%2Fwechat%2Fopenid.ashx%3Fwx%3Dfindangel%26type%3D1%26Url%3Dhttp%253A%252F%252Fyuyue.tianshizhiwen.org%252Fstatic%252FMobileClient%252FSaler%252FstaffAuth.html&response_type=code&scope=snsapi_base&state=O#wechat_redirect")

def mypation(req):
    return HttpResponseRedirect("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxcf86e59e9c228363&redirect_uri=http%3A%2F%2Fwx.yuemia.com%2Fwechat%2Fopenid.ashx%3Fwx%3Dfindangel%26type%3D1%26Url%3Dhttp%253A%252F%252Fyuyue.tianshizhiwen.org%252Fstatic%252FMobileClient%252FSaler%252FMyPatient.html&response_type=code&scope=snsapi_base&state=O#wechat_redirect")