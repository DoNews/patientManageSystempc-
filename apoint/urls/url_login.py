
from apoint.Views.view_user import *

from django.conf.urls import url
urlpatterns = [
    url(r'^login', userlogin),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'login.html'}),
        ]