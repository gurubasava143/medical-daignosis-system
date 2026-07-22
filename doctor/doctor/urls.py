"""
URL configuration for doctor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from patient import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path("insertuserreg",views.insertuserreg,name="insertuserreg"),
    path("showusereg", views.showusereg, name="showusereg"),
    path('deluserreg/<int:pk>/', views.deluserreg, name='deluserreg'),

    path("insertsymptom",views.insertsymptom,name="insertsymptom"),
    path("showsymptom", views.showsymptom, name="showsymptom"),
    path('delsymptom/<int:pk>/', views.delsymptom, name='delsymptom'),

    path("daignosis1",views.daignosis1,name="daignosis1"),
    path('showdiagnosis',views.showdiagnosis,name='showdiagnosis'),
    path('deldiagnosis/<int:pk>/', views.deldiagnosis, name='deldiagnosis'),

    path("insertprescript",views.insertprescript,name="insertprescript"),
    path("showprescription", views.showprescription, name="showprescription"),
    path('delprescription/<int:pk>/', views.delprescription, name='delprescription'),
    path('viewprescriptiondetail/<int:pk>/', views.viewprescriptiondetail, name='viewprescriptiondetail'),


    path("insertpayment",views.insertpayment,name="insertpayment"),
    path("showmpayment", views.showmpayment, name="showmpayment"),
    path('delpayment/<int:pk>/', views.delpayment, name='delpayment'),

    path("insertpatient",views.insertpatient,name="insertpatient"),
    path("showmpatient", views.showmpatient, name="showmpatient"),
    path('delpatient/<int:pk>/', views.delpatient, name='delpatient'),

    path("insertnotification",views.insertnotification,name="insertnotification"),
    path("showmnotification", views.showmnotification, name="showmnotification"),
    path('delnotification/<int:pk>/', views.delnotification, name='delnotification'),
    path('viewnotificationdetail/<int:pk>/', views.viewnotificationdetail, name='viewnotificationdetail'),

    path("insertmedihistory", views.insertmedihistory, name="insertmedihistory"),
    path("showmedicalhistory", views.showmedicalhistory, name="showmedicalhistory"),
    path('delmedicalhistory/<int:pk>/', views.delmedicalhistory, name='delmedicalhistory'),

    path("insertlabtest", views.insertlabtest, name="insertlabtest"),
    path("showlabtest", views.showlabtest, name="showlabtest"),
    path('dellabtest/<int:pk>/', views.dellabtest, name='dellabtest'),

    path("insertlabresult", views.insertlabresult, name="insertlabresult"),
    path("showlabresult", views.showlabresult, name="showlabresult"),
    path('dellabresult/<int:pk>/', views.dellabresult, name='dellabresult'),

    path("insertfeedback", views.insertfeedback, name="insertfeedback"),
    path('showfeedback',views.showfeedback,name='showfeedback'),
    path('delfeedback/<int:pk>/',views.delfeedback,name='delfeedback'),

    path("insertdoctor", views.insertdoctor, name="insertdoctor"),
    path("showdoctor", views.showdoctor, name="showdoctor"),
    path('deldoctor/<int:pk>/', views.deldoctor, name='deldoctor'),

    path("insertlogin", views.insertlogin, name="insertlogin"),
    path("showlogin", views.showlogin, name="showlogin"),
    path('dellogin/<int:pk>/', views.dellogin, name='dellogin'),

    path("", views.showindex, name="showindex"),
    path("logcheck", views.logcheck, name="logcheck"),
    path("logout", views.logout, name="logout"),
    path("forgot_password", views.forgot_password, name="forgot_password"),
    path("admin_home", views.admin_home, name="admin_home"),
    path("doctor_home", views.doctor_home, name="doctor_home"),
    path("patient_home", views.patient_home, name="patient_home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
