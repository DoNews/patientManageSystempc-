
from apoint.Views.view_wechat import *

from django.conf.urls import url
urlpatterns = [
    url(r'^order$',order),
    url(r'^checkUser', checkUser),
    url(r'^reg$', reg),
    url(r'^mypation$', mypation),
]