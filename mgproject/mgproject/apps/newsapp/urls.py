from django.urls import re_path,path
from . import views
urlpatterns=[
    re_path('^$', views.IndexView.as_view(), name='index'),
    path('list/<int:id>/<int:page_num>/',views.ChannelView.as_view()),
    re_path('^detail/(?P<article_id>\d+)/$',views.DetailView.as_view()),
    path('news/<int:id>',views.ChannelView.as_view())
]

