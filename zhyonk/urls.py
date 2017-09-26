# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.contrib import admin

from wechat.views import IndexView, personal, checkin, GetUserInfoView, WxSignature, TestView,AuthView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', IndexView.as_view()),
    url(r'^personal/', personal),
    url(r'^checkin/', checkin),
    url(r'^auth/$', AuthView.as_view(), name='wx_auth'),  # 获取用户信息

# 授权
    url(r'^auth/$', AuthView.as_view(), name='wx_auth'),
    # 获取用户信息
    url(r'^code/$', GetUserInfoView.as_view(), name='get_user_info'),
    # 微信接口配置信息验证
    url(r'^$', WxSignature.as_view(), name='signature'),
    # 测试
    url(r'^test/$', TestView.as_view(), name='test_view'),
]
