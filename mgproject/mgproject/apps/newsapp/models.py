from django.db import models

# Create your models here.
from mgproject.utils.basemodels import BaseModel

class NewsChannel(BaseModel):
    """新闻频道"""
    name = models.CharField(max_length=30,unique=True,verbose_name='频道名称')
    url = models.CharField(default='',null=True,blank=True,max_length=50, verbose_name='频道页面链接')

    class Meta:
        db_table = 't_news_channel'
        verbose_name = '新闻频道'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class NewsCategory(BaseModel):
    """新闻类别"""
    name = models.CharField(max_length=10,verbose_name='名称')
    sequence = models.IntegerField(verbose_name='排序')
    channel = models.ForeignKey(NewsChannel,on_delete=models.PROTECT)


    class Meta:
        db_table = 't_news_category'
        verbose_name = '新闻类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Article(BaseModel):
    """文章"""
    title = models.CharField(max_length=100,unique=True,verbose_name='文章标题')
    content = models.TextField(verbose_name='文章内容')
    default_img = models.ImageField(verbose_name='首页图片')
    starcount = models.IntegerField(default=0,verbose_name='点赞量')
    commentcount = models.IntegerField(default=0,verbose_name='评论量')
    category = models.ForeignKey(NewsCategory,on_delete=models.PROTECT, verbose_name='从属类别')

    class Meta:
        db_table = 't_news_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ArticleImage(BaseModel):
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='图片')

    class Meta:
        db_table = 't_article_image'
        verbose_name = 'article图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.article.title, self.id)