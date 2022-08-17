from django.db import models
# Create your models here
from mgproject.utils.basemodels import BaseModel

class QQAuthUser(BaseModel):

    """QQ登录⽤户数据"""
    user = models.ForeignKey('userapp.User',on_delete=models.CASCADE, verbose_name='⽤户')
    openid = models.CharField(max_length=64, verbose_name='openid',db_index=True)
    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录⽤户数据'
        verbose_name_plural = verbose_name




