# -*- coding: utf-8 -*-
# @Time    : 2022/8/6 0:21
# @Author  : Ricky
# @IDE: PyCharm
from django.utils.deprecation import MiddlewareMixin

class md1(MiddlewareMixin):

    def process_request(self, request):
        print("MD1里面的 process_request")