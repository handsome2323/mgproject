from django import http
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from .models import NewsChannel, Article

from django.core.paginator import Paginator, EmptyPage


class DetailView(View):
    def get(self,request,article_id):
        """
        新闻详情
        :param request:
        :param article_id:
        :return:
        """
        try:

            article1 = Article.objects.all()


            print('所有文章~',article1)
            article = Article.objects.get(id=article_id)

            # print('所有的文章>>>>>>>>>>>>', article)
        except Article.DoesNotExist:
            return http.HttpResponseNotFound('未找到article_id对应文章')

        print(article)
        return render(request,'newsapp/detail.html',{'article':article})



class IndexView(View):
    def get(self,request,channel_id=1,page_num=1):
        """新闻列表展示功能"""
        try:
            # 获取NewsChannel对象
            newschannel = NewsChannel.objects.get(id=channel_id)

        except NewsChannel.DoseNotExist:
            return http.HttpResponseNotFound('未找到channel_id')
        else:

            # 获取当前频道下的所有类别id
            category_id_list = [category.id for category in newschannel.newscategory_set.all() if category]

        # 查看当前频道下的所有文章
        articles = Article.objects.filter(category_id__in=category_id_list).order_by('id')



        # 创建分页器对象
        page_obj = Paginator(articles,3)

        # 获取当前页数据
        try:
            page_articles = page_obj.page(page_num)

        except EmptyPage:
            return http.HttpResponseNotFound('未找到相应page_num')

        return render(request,'newsapp/index.html',context={'articles':page_articles,'channel_id':channel_id})





class ChannelView(View):
    def get(self, request, id, page_num=1):
        """新闻列表展示功能"""
        try:
            # 获取NewsChannel对象
            newschannel = NewsChannel.objects.get(id=id)

        except NewsChannel.DoseNotExist:
            return http.HttpResponseNotFound('未找到channel_id')
        else:

            # 获取当前频道下的所有类别id
            category_id_list = [category.channel_id for category in newschannel.newscategory_set.all() if category]

        # 查看当前频道下的所有文章
        articles = Article.objects.filter(category_id__in=category_id_list).order_by('id')

        print('这是文章~~~~',articles)
        # 创建分页器对象
        page_obj = Paginator(articles, 3)

        # 获取当前页数据
        try:
            page_articles = page_obj.page(page_num)

        except EmptyPage:
            return http.HttpResponseNotFound('未找到相应page_num')

        return render(request, 'newsapp/index.html',context={'articles': page_articles, 'channel_id': id})









