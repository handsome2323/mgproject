import os
from random import sample

from alipay import AliPay
from django import http
from django.conf import settings
from django.db import DataError
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views.generic.base import View

from .models import OrderInfo, Payment
from mgproject.utils.views import LoginRequiredJSONMixin
import json

from django.utils.deprecation import MiddlewareMixin
#微信支付
from wechatpayv3 import WeChatPay
from string import ascii_letters, digits
from wechatpayv3 import SignType, WeChatPay, WeChatPayType
class PaymentStatusView(LoginRequiredJSONMixin,View):
    def get(self,request):
        """
        查询并保存支付结果
        :param request:
        :return:
        """
        # 接收参数
        params_dict = request.GET.dict()

        # 校验参数（验证签名：判断当前是否支付宝平台重定向过来的请求）
        sign = params_dict.pop('sign')

        # 创建支付宝支付对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=open(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem")).read(),
            alipay_public_key_string=open(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/alipay_public_key.pem")).read(),
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )

        flag = alipay.verify(params_dict,sign)

        if flag:  # 正常请求

            # 获取订单号
            order_id = params_dict.get('out_trade_no')
            # 获取支付宝交易流水号
            trade_no = params_dict.get('trade_no')
            # 保存支付结果
            try:
                Payment.objects.create(order_id=order_id,trade_id=trade_no)
            except DataError:
                return http.HttpResponseForbidden('保存支付结果失败')
            # 更新订单表中支付状态
            OrderInfo.objects.filter(order_id=order_id,status=1).update(status=2)

            # 响应页面结果
            return render(request,'payment/pay_success.html',{'trade_no':trade_no})

        else:
            return http.HttpResponseForbidden('非正常请求')




class PaymentView(View):
    def post(self,request):
        """
        获取支付宝支付扫码链接地址
        :param request:
        :return:
        """
        if not request.user.is_authenticated:
            next = request.POST.get('next','')
            # return render(request, 'userapp/login.html', {'next': next})

            return JsonResponse({'code': 4003, 'errmsg': '用户未登录'})
        # 接收参数 '{"k":"v"}'  ---> {"k":"v"}
        params_str = request.body.decode()
        # 校验参数
        if not params_str:
            return JsonResponse({'code':4001,'errormsg':'缺少必传参数'})
        print('这是params_str',params_str,type(params_str))
        dict_params = json.loads(params_str)
        #支付宝支付
        if dict_params['pay_method']==1:
            article_id = dict_params['article_id']
            pay_method = dict_params['pay_method']
            total_amount = dict_params['pay_amount']
            #生成订单
            user = request.user
            # 生成订单编号：年月日时分秒+用户编号
            order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%03d' % user.id)
            try:
                order = OrderInfo.objects.create(order_id=order_id,user=user,pay_method=pay_method,total_amount=total_amount,article_id=article_id)
            except DataError:
                return JsonResponse({'code':4002,'errormsg':'生成订单失败'})

            # 调用支付接口获取支付链接地址
            # 创建支付宝支付对象
            alipay = AliPay(
                appid=settings.ALIPAY_APPID,
                app_notify_url=None,  # 默认回调url
                app_private_key_string=open(
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem")).read(),
                alipay_public_key_string=open(
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/alipay_public_key.pem")).read(),
                sign_type="RSA2",
                debug=settings.ALIPAY_DEBUG
            )

            # 生成登录支付宝连接
            order_string = alipay.api_alipay_trade_page_pay(
                out_trade_no=order_id,
                total_amount=str(order.total_amount),
                subject="芒果头条%s" % order_id,
                return_url=settings.ALIPAY_RETURN_URL,
                notify_url=settings.ALIPAY_RETURN_URL
            )
            print('这是order_string',order_string)


            # 响应结果
            # 响应登录支付宝链接
            # 真实环境电脑网站支付网关：https://openapi.alipay.com/gateway.do? + order_string
            # 沙箱环境电脑网站支付网关：https://openapi.alipaydev.com/gateway.do? + order_string
            alipay_url = settings.ALIPAY_URL + order_string
            return JsonResponse({'code': 200, 'errormsg': 'OK', 'alipay_url': alipay_url})

        #调用微信支付接口
        if dict_params['pay_method']==2:
            #创建微信支付对象
            wxpay = WeChatPay(
                wechatpay_type=WeChatPayType.H5,
                # 微信支付商户号（直连模式）或服务商商户号（服务商模式，即sp_mchid)
                mchid=MCHID,
                # 商户证书私钥
                private_key=PRIVATE_KEY,
                # 商户证书序列号
                cert_serial_no=CERT_SERIAL_NO,
                # API v3密钥
                apiv3_key=APIV3_KEY,
                # APPID，应用ID或服务商模式下的sp_appid
                appid=APPID,
                # 回调地址，也可以在调用接口的时候覆盖
                notify_url=NOTIFY_URL,
                # 回调地址，也可以在调用接口的时候覆盖
                cert_dir=None,
                logger=None,
                partner_mode=False,
                #代理地址
                proxy=None)
            out_trade_no = ''.join(sample(ascii_letters + digits, 8))
            description = 'demo-description'
            amount = 1
            scene_info = {'payer_client_ip': '1.2.3.4', 'h5_info': {'type': 'Wap'}}
            code, message = wxpay.pay(
                description=description,
                out_trade_no=out_trade_no,
                amount={'total': amount},
                scene_info=scene_info
            )
            return JsonResponse({'code': code, 'message': message})
