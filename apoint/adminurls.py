from django.conf.urls import url,include
from django.contrib import admin

from apoint.Views.adminviews import *
urlpatterns = [
    url(r'adminindex', adminindex),
    url(r'^adminpationsview', adminpationsview),
    url(r'^hospital', hospital),
    url(r'^thirdpart', thirdpart),
    url(r'^adminchart', adminchart),
    url(r'^adminaccount', adminaccount),
    url(r'^staffedit', staffedit),
    url(r'^editHospital', editHospital),
    url(r'^staffaddnew', staffaddnew),
    url(r'^hospview', hospview),
    url(r'^thirdpop', thirdpop),
    url(r'^refenpei', refenpei),
    url(r'^staff$', staff),
    url(r'^addCustomer$',addCustomer),
    url(r'^addCustomerAction',addCustomerAction),

]