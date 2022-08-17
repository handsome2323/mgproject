from django.urls import re_path,path

from . import views

urlpatterns=[
    re_path('^payment/$',views.PaymentView.as_view()),
    re_path('^payment/status/$', views.PaymentStatusView.as_view()),

]