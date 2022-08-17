from django.db import models

# Create your models here.
from mgproject.utils.basemodels import BaseModel


class DingdingAuthUser(BaseModel):

    """QQ登录⽤户数据"""
    user = models.ForeignKey('userapp.User',on_delete=models.CASCADE, verbose_name='⽤户')
    openid = models.CharField(max_length=255, verbose_name='openid',db_index=True)
    class Meta:
        db_table = 'tb_oauth_dingding'
        verbose_name = '钉钉登录⽤户数据'
        verbose_name_plural = verbose_name
