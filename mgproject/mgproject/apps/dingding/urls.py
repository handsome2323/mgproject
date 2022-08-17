from django.urls import re_path,path
from . import views
urlpatterns=[
    # re_path('^dingding/login/$', views.DingdingLoginURLView.as_view()),
    re_path('^ding_back/$',views.DingdingAuthUserView.as_view())

]

