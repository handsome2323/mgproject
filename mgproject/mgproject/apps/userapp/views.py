import json
import re
from sqlite3 import DatabaseError

from django import http
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic.base import View

from .models import User

from mgproject.utils.exceptions import Forbbiden


class UserCenterView(View):


    def get(self,request):
        """
        显示用户中心页面
        :param request:
        :return:
        """
        return render(request, 'userapp/user_center.html')

        # 判断当前访客是否已登录
        # if request.user.is_authenticated:
        #     return render(request,'userapp/user_center.html')
        # else:
        #     return redirect(reverse('newsapp:index'))


class RegisterView(View):
    def get(self,request):
        return render(request,'userapp/register.html')

    def post(self,request):
        #接受数据

        #校验参数，完整(参数校验，格式校验)

        #保存注册参数(入库操作)

        username=request.POST.get('username')

        phone=request.POST.get('phone')

        password=request.POST.get('password')

        # 判断参数是否⻬全
        if not all([username, password, phone]):
            raise Forbbiden('缺少必传参数')
        # 判断⽤户名是否是5-8个字符
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]{4,7}$', username):
            raise Forbbiden('请输⼊5-8个字符的⽤户名')
        # 判断密码是否是3-8个字符
        if not re.match(r'^[0-9a-zA-Z]{3,8}$', password):
            raise Forbbiden('请输⼊3-8位的密码')
        # 判断⼿机号是否合法
        if not re.match(r'^1[3589]\d{9}$', phone):
            raise Forbbiden('请输⼊正确的⼿机号码')

        try:

            user=User.objects.create_user(username=username,password=password,phone=phone)

        except DatabaseError:

            return render(request,'userapp/register.html',{'reg_error_msg':'注册失败'})



        #状态保持

        login(request,user)


        # 返回响应结果



        return redirect(reverse('newsapp:index'))



class UsernameCount(View):


    def get(self,request,username):
        '''

        查询用户当前的记录数

        :param request:
        :param uname:
        :return:
        '''

        count = User.objects.filter(username=username).count()
        print('--->', count)

        return JsonResponse({'code':200,'errormsg':'OK','count':count})

#退出登录
class Logout(View):

    def get(self,request):

        logout(request)

        return redirect(reverse('newsapp:index'))

#校验手机号码
class check_phone(View):
    def get(self,request,phone):

        count = User.objects.filter(phone=phone).count()

        return JsonResponse({'code': 200, 'errormsg': 'OK', 'count': count})



#登录功能
class LoginView(View):
    '''
    用户名登录视图

    '''
    #显示登录首页
    def get(self,request):

        next = request.GET.get('next', '')
        print('这是next',next)
        return render(request, 'userapp/login.html',{'next':next})


    #处理登录请求
    def post(self,request):

        next = request.POST.get('next', '')
        # 接收参数
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        remember = request.POST.get('remember', '')


        #校验参数

        if not all([username,password,remember]):
            return http.HttpResponseForbidden('缺少必传参数')

        # # 判断用户名是否是5-8个字符
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]{4,7}$', username):
            return http.HttpResponseForbidden('请输入5-8个字符的用户名')

        # 判断密码是否是3-8个字符
        if not re.match(r'^[0-9a-zA-Z]{3,8}$', password):
            return http.HttpResponseForbidden('请输入3-8位的密码')

        #认证参数是否正确
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'userapp/login.html', {'login_error': '用户名或密码错误'})


        #状态保持

        login(request,user)

        if remember != 'on':
            # 关闭浏览器失效
            request.session.set_expiry(0)
        else:
            # 14天有效期
            request.session.set_expiry(None)

        if next:
            return redirect(next)
            # 响应结果
        return redirect(reverse('newsapp:index'))
class EmailView(View):


    def post(self,request):
        '''
        保存当前登录用户邮箱保存地址
        :param request:
        :return:
        '''

        #接受参数，校验参数

        params = request.body.decode()

        print(params)


        #校验参数
        if params is None:
            return JsonResponse({'code':4001,'errormsg':'缺少必传参数'})

        # 保存数据


        # 转型
        dict_params = json.loads(params)

        count = User.objects.filter(id=dict_params['userid']).update(email=dict_params['email'])

        User.objects.create()


        #响应结果
        if count>0:
            return JsonResponse({'code':200,'errormsg':'OK'})

        return JsonResponse({'code':500,'errormsg':'Error'})



