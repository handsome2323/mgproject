import os

from django.conf import settings
from django.core.paginator import Paginator
from django.template import loader
from django.utils import timezone
from .models import NewsChannel, Article


def static_index_html():
    """
    将新闻首页实现页面静态化处理
    :return:
    """
    # 准备base.html需要数据
    channels = NewsChannel.objects.order_by('id')

    # 获取NewsChannel对象
    newschannel = NewsChannel.objects.get(id=1)

    # 获取当前频道下的所有类别id
    category_id_list = [category.id for category in newschannel.newscategory_set.all() if category]

    # 查看当前频道下的所有文章
    articles = Article.objects.filter(category_id__in=category_id_list).order_by('id')

    # 创建分页器对象
    page_obj = Paginator(articles, 3)

    # 获取当前页数据
    page_articles = page_obj.page(1)

    # 准备页面数据
    context = {
        'articles': page_articles,
        'channel_id': 1,
        'channels':channels
    }

    # 获取首页模板文件
    template = loader.get_template('newsapp/index.html')
    # 渲染首页html字符串
    html_text = template.render(context)
    # 将首页html字符串写入到指定目录，命名'index.html'
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)

    print(timezone.localtime().strftime('%H:%M:%S'))


