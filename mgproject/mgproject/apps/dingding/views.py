import base64
import hmac
import json
import re
import time
import urllib
import jwt
import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import os
# Create your views here.
from django.urls import reverse
from django_redis import get_redis_connection
from userapp.models import User
from django.views.generic.base import View
from .models import DingdingAuthUser
from hashlib import sha256
from .utils import generate_secret_openid,check_secret_openid
from django import http
from django.contrib.auth import login
from .models import DingdingAuthUser

class DingdingLoginURLView(View):
    # 构建一个钉钉类

        # 拼接url
        # 构造钉钉登录url
    def ding_url(self,request):
        appid = 'dingoalw7fffrv2a8on3ss'  # 应用中的appid
        redirect_uri = 'http://127.0.0.1:8000/ding_back/'  # 钉钉返回信息的回调地址
        dingding_url='https://oapi.dingtalk.com/connect/qrconnect?appid=' + appid + '&response_type=code&scope=snsapi_login&state=STATE&redirect_uri=' + redirect_uri
        print('这是dingdingurl',dingding_url)
        return JsonResponse({'code': 200, 'errormsg': 'OK', 'dingding_url': dingding_url})


    # 构造钉钉回调方

class DingdingAuthUserView(View):
    def get(self,request):
        # 获取code
        code = request.GET.get("code",'')
        if not code:
            return http.HttpResponseForbidden('缺少code参数')
        print('这是code',code)
        t = time.time()
        # 时间戳
        timestamp = str((int(round(t * 1000))))
        appSecret = 'imK8TEF_hrJ0i5CSQBAm3gZ5pVokcdV_1oewvys5vtN30dI_9txQoW6Gzl_8QkbG'
        # # 构造签名
        signature = base64.b64encode(hmac.new(appSecret.encode('utf-8'), timestamp.encode('utf-8'), digestmod=sha256).digest())
        # # 请求接口，换取钉钉用户名
        payload = {'tmp_auth_code': code}
        headers = {'Content-Type': 'application/json'}
        appid = 'dingoalw7fffrv2a8on3ss'
        res = requests.post(
            'https://oapi.dingtalk.com/sns/getuserinfo_bycode?signature=' + urllib.parse.quote(
                signature.decode("utf-8")) + "&timestamp=" + timestamp + "&accessKey=" + appid,
            data=json.dumps(payload), headers=headers)  # accessKey=appid
        # 返回的用户信息
        res_dict = json.loads(res.text)
        # print('这是resdict',res_dict)
        # name = res_dict['user_info']['nick']
        print('这是真实的openid',res_dict['user_info']['dingId'])

        # # 判断钉钉用户对象是否存在
        try:
            dingding_obj = DingdingAuthUser.objects.get(openid=res_dict['user_info']['dingId']).first()
            print('钉钉用户对象', dingding_obj)
        except:
            # 加密openid数据
            sec_openid = generate_secret_openid(res_dict['user_info']['dingId'])

            print('这是加密后的sec_openoid',sec_openid)

            #传递加密数据给用户绑定页面
            return render(request,'dingding_user/dingding_user.html',{'sec_openid':sec_openid})

        else:

            user = dingding_obj.user
            # 状态保持
            login(request,user)
            # 响应结果
            return redirect(reverse('newsapp:index'))


    def post(self,request):
        """
        将当前访问QQ用户绑定项目用户
        :param request:
        :return:
        """
        # 接收参数
        sec_openid = request.POST.get('sec_openid','')



        phone = request.POST.get('phone', '')
        sms_code_client = request.POST.get('msgcode', '')
        pwd = request.POST.get('password', '')

        # 校验参数(非空校验/格式校验/一致性校验)
        # 判断参数是否齐全
        if not all([phone, pwd, sms_code_client, sec_openid]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断手机号是否合法
        if not re.match(r'^1[35789]\d{9}$', phone):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断密码是否合法
        if not re.match(r'^[0-9A-Za-z]{3,8}$', pwd):
            return http.HttpResponseForbidden('请输入3,8位的密码')

        # 判断短信验证码是否一致
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % phone)
        if sms_code_server is None:
            return render(request, 'dingding_user/dingding_user.html', {'sms_code_errmsg': '无效的短信验证码'})
        if sms_code_client != sms_code_server.decode():
            return render(request, 'dingding_user/dingding_user.html', {'sms_code_errmsg': '输入短信验证码有误'})


        # 绑定用户

        # 判断当前QQ用户是否合法(解密openid数据)
        openid = check_secret_openid(sec_openid)
        print('这是校验后的openid',openid)


        if openid is None:
            return render(request, 'dingding_user/dingding_user.html', {'openid_errmsg': 'openid已经失效'})

        # 获取项目用户
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            # 创建项目新用户
            user = User.objects.create_user(username=phone,password=pwd,phone=phone)
        else:
            # 判断项目用户密码是否正确
            if not user.check_password(pwd):
                return render(request,'dingding_user/dingding_user.html',{'qq_login_errmsg':'用户名或密码错误'})

        # 绑定用户
        try:
            DingdingAuthUser.objects.create(user=user,openid=openid)
            print('解密后的openid', openid)
        except Exception as e:
            print(e)
            return render(request, 'dingding_user/dingding_user.html', {'reg_error_msg': '用户绑定失败'})

        # 状态保持
        login(request,user)

        # 响应结果
        return redirect(reverse('newsapp:index'))


