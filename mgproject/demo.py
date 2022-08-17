# a=[1,12,22]
# a.pop(0)
# print(a)


# a=1
# v=2 if a else 2
# print(v)
# dict={}
# dictname = dict.fromkeys(list,value=None)
# print(dictname)

# knowledge = ['语文', '数学', '英语']
# scores = dict.fromkeys(knowledge, [])
# print(scores)

# import os
# a=input(os)
# print(a)

# import time
# t=time.time()
# print(t)
# print(round(t))
# #
#
# timestamp = str((int(round(t * 1000))))
#
# print(timestamp)

# appid = 'dingoalw7fffrv2a8on3ss'  # 应用中的appid
# redirect_uri = 'http://127.0.0.1:8000/ding_back/'  # 钉钉返回信息的回调地址
# dingding_url='https://oapi.dingtalk.com/connect/qrconnect?appid=' + appid + '&response_type=code&scope=snsapi_login&state=STATE&redirect_uri=' + redirect_uri
# timestamp = str((int(round(t * 1000))))
# print('这是dingdingurl',dingding_url)

# a=1
# try:
#     if a==1:
#         print('111')
# except:
#     print('333')
#
# else:
#     print('222')

# appid = 'dingoalw7fffrv2a8on3ss'  # 应用中的appid
# redirect_uri = 'http://127.0.0.1:8083/ding_back/'  # 钉钉返回信息的回调地址
# dingding_url='https://oapi.dingtalk.com/connect/qrconnect?appid=' + appid + '&response_type=code&scope=snsapi_login&state=STATE&redirect_uri=' + redirect_uri
# print('这是dingdingurl',dingding_url)


# print(len('eyJhbGciOiJIUzUxMiIsImlhdCI6MTY0NTg2OTQwOSwiZXhwIjoxNjQ1ODcwMDA5fQ.eyJvcGVuaWQiOiIkOkxXQ1BfdjE6JFFDUXFEMHdnWEtzcEV2TXBWZ2UvR3c9PSJ9.fEgQANPPtYbn0gp8IHBHGozU_8tjBoqUYBS-hpNFq27exEZgUp39E4Z3ygZAIPFaDNTbiQcQjcM4dxS_mB'))


# from django.conf import settings
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
#
#
# def generate_secret_openid(openid):
#     """
#     签名openid
#     :param openid: 用户的openid
#     :return: access_token
#     """
#     # 创建序列化器对象给数据加密
#     serializer = Serializer(settings.SECRET_KEY,expires_in=600)
#     data = {'openid': openid}
#     token = serializer.dumps(data)
#     return token.decode()
#
# def check_secret_openid(sec_openid):
#     """
#     反解、反序列化access_token_openid
#     :param access_token_openid: openid密文
#     :return: openid明文
#     """
#     # 创建序列化器对象：序列化和反序列化的对象的参数必须是一模一样的
#     s = Serializer(settings.SECRET_KEY, expires_in=600)
#
#     # 反序列化openid密文
#     try:
#         data = s.loads(sec_openid)
#     except BadData: # openid密文过期
#         return None
#     else:
#         # 返回openid明文
#         return data.get('openid')


# a=1
#
# try:
#     print('1')
#     if a ==b:
#         pass
# except:
#     pass




# class test:
#     def __init__(self,file):
#         with open(file,'a',encoding='utf-8')as f:
#             f.write('aaa')
#
#             self.f=f
#
#     def kobe(self):
#         print(self.f)
#
# a=test('kobe.txt')
# a.kobe()

#
# import subprocess
# def command(a):
#     command_data = subprocess.run(a,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='GBK',shell=True)
#
#     print(command_data)
# #
# #
# command('python3')
# a='hello world'
# b=a.encode('utf-8')
# print(b.decode('utf-8'))

import os
import threading
def kobe():
    while 1:
        for i in range(200):
            print(i)
for i in range(100):
    t= threading.Thread(target=kobe)
    t.start()