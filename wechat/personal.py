#_author_='zhyonk'
#-*- coding:utf-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render

from wechat.auth_view import AuthView as BaseView

def personal(request):
    request.encoding = 'utf-8'
    context = {}
    user_info = request.session['user']
    context['nickname'] = user_info['info']['nickname']
    context['headimgurl'] = user_info['info']['headimgurl']
    user_info_json = json.dumps(user_info)
    result = HttpResponse(user_info_json, content_type="application/json")
    return result