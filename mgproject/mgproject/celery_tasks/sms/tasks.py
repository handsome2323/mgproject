import os
import sys

# 添加导包路径
B_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print('这是导包路径',B_DIR)
# print(B_DIR)
sys.path.insert(0, os.path.join(B_DIR, 'utils'))
sys.path.insert(1, B_DIR)

import logging

# from mgproject.celery_tasks.main import celery_app
from celery import Celery

celery_app=Celery('mangguo')


# 加载配置文件
celery_app.config_from_object('celery_tasks.config')

# 加载异步任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])

# celery_app

# 为celery使用django配置文件进行设置
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.dev')

# from utils.huyi_sms.sms3 import send_sms_code

from urllib.request import urlopen
from urllib.parse import urlencode
import json

def send_sms_code(smscode,phone):
    # APIID(用户中心【验证码通知短信】-【产品纵览】查看)
    account = 'C77581811'
    # APIKEY(用户中心【验证码通知短信】-【产品纵览】查看)
    password = '7bd97ea61c750ea133fdd7a8afcc21cd'
    text = '您的验证码是：'+smscode+'。请不要把验证码泄露给其他人。'
    data = {'account': account, 'password': password, 'content': text, 'mobile': phone, 'format': 'json'}
    req = urlopen(url='https://106.ihuyi.com/webservice/sms.php?method=Submit',data=urlencode(data).encode())
    content = req.read().decode()
    print(content)
    # code等于2代表提交成功，否则提交失败
    # smsid等于0代表提交失败，否则显示长度20流水号
    # b'{"code":2,"msg":"\xe6\x8f\x90\xe4\xba\xa4\xe6\x88\x90\xe5\x8a\x9f","smsid":"16063783563405105174"}'

    return json.loads(content)

logger = logging.getLogger('django')


@celery_app.task(name='huyi_send_sms_code')
def huyi_send_sms_code(phone, smscode_str):
    """
    发送短信异步任务
    :param phone: 手机号
    :param smscode: 短信验证码
    :return: 成功 code=2 或 失败 smsid=0
    """

    try:
        # 调用外部接口执行发送短信任务
        ret = send_sms_code(smscode_str, phone)

    except Exception as e:
        logger.error(e)

    if ret.get('code') != 2:
        logger.error(e)

    return ret.get('code', None)