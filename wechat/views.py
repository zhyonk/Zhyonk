# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseServerError, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from models import Users as User, UserSerializer
from robot import robot
from wechat.auth_view import AuthView as BaseView
from wechat.wechat_api import WechatApi


class IndexView(BaseView):
    def get(self, request):
        request.encoding = 'utf-8'
        context = {}
        user_info = request.session['user']

        return render(request, 'index.html', context)





# 接收请求数据
def checkin(request):
    request.encoding = 'utf-8'
    context = {}
    context['content'] = "11"

    return render(request, 'check.html', context)


class WecahtApiView(View):
    # 填入公众号appid, appsecret
    APPID = 'wx3fcb154832732b75'
    APPSECRET = '6961c68cc55aad7fc460a03fb08b281c'
    HOST = 'http://zhyonk.tunnel.echomod.cn'

    wechat_api = WechatApi(appid=APPID, appsecret=APPSECRET)


class WxSignature(View):
    pass  # 非重点省略


class AuthView(WecahtApiView):
    def get(self, request):

        path = request.GET.get('path')
        if path:
            if 'user' in request.session:
                return redirect(path)
            else:
                red_url = '%s%s?path=%s' % (self.HOST, reverse('get_user_info'), path)
                redirect_url = self.wechat_api.auth_url(red_url, scope='snsapi_base')
                return redirect(redirect_url)
        else:
            return Http404('parameter path not founded!')


class GetUserInfoView(WecahtApiView):
    def get(self, request):
        redir_url = request.GET.get('path')
        code = request.GET.get('code')

        if redir_url and code:

            # 获取网页授权access_token
            token_data, error = self.wechat_api.get_auth_access_token(code)

            if error:
                print error
                return HttpResponseServerError('get access_token error')

            # 获取用户信息信息

            user_info, error = self.wechat_api.get_user_info(token_data['access_token'], token_data['openid'])

            if error:
                print error
                return HttpResponseServerError('get userinfo error1')

            # 存储用户信息
            user = self._save_user(user_info)
            if not user:
                return HttpResponseServerError('save userinfo error2')

            # 用户对象存入session
            request.session['user'] = user

            # 跳转回目标页面
            return redirect(redir_url)

        # 用户禁止授权后怎么操作
        else:
            return Http404('parameter path or code not founded!!')

    def _save_user(self, data):
        user = User.objects.filter(openid=data['openid'])

        # 没有则存储用户数据，有返回用户数据的字典
        if 0 == user.count():
            user_data = {
                'nick': data['nickname'].encode('iso8859-1').decode('utf-8'),
                'openid': data['openid'],
                'avatar': data['headimgurl'],
                'info': self._user2utf8(data),
            }

            if 'unionid' in data:
                user_data.update({'unionid':data.unionid})

            try:
                new_user = User(**user_data)
                new_user.save()

                user_data.update({'id': new_user.id})
                return user_data
            except Exception, e:
                print e

            return None
        else:
            # 把User对象序列化成字典，具体看rest_framework中得内容
            result = UserSerializer(user[0]).data
            return result

    # 解决中文显示乱码问题
    def _user2utf8(self, user_dict):
        utf8_user_info = {
            "openid": user_dict['openid'],
            "nickname": user_dict['nickname'].encode('iso8859-1').decode('utf-8'),
            "sex": user_dict['sex'],
            "province": user_dict['province'].encode('iso8859-1').decode('utf-8'),
            "city": user_dict['city'].encode('iso8859-1').decode('utf-8'),
            "country": user_dict['country'].encode('iso8859-1').decode('utf-8'),
            "headimgurl": user_dict['headimgurl'],
            "privilege": user_dict['privilege'],
        }

        if 'unionid' in user_dict:
            utf8_user_info.update({'unionid': user_dict['unionid']})

        return utf8_user_info


class TestView(BaseView):
    def get(self, request):
        return render(request, 'index.html')