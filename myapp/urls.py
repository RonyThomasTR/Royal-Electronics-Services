from django.contrib import admin
from django.urls import path
from myapp.views import *
from . import views
app_name='myapp'

urlpatterns = [
    path('',myview),
    path('login/',logins),
    path('signin/',signin),
    path('appointment/',appointment),
    path('prof/',profile),
    path('add/',add_staff),
    path('vwdet/',vwdetails),
    path('log/',logouts),
    path('det/',vwdetails),
    path('prof/',profile),
    path('edited/',editprofile),
    path('appo/',userapointvw),
    path('dele/',delaccount),
    path('hm/',home),
    path('bk/',back),
    path('ushm/',usrhm),
    path('stm/',sthm),
    path('adm/',adhm),
    path('vst/',vwstf),
    path('acce/<int:id>/', accept),
    path('waitc/<int:id>/', waitforconfirm),
    path('onprogres/<int:id>/', onprogress),
    path('rejected/<int:id>/', reject),
    path('delstf/<int:id>/',delacount),
    path('estim/<int:id>/',estimation),
    path('estm/<int:appointment_id>/', estimation_page),
    path('estima/<int:appointment_id>/', make_estimation),
    path('userestm/<int:id>/',view_estimation),
    path('backappoint/',backappoint_view),
    path('rejection/<int:id>/', rejection),
    # path('accepthome/<int:id>',homeservice),
]