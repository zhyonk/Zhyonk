# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
import urllib

from django.views.generic import View
from django.shortcuts import redirect

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User, Group
from rest_framework import serializers


# Create your models here.
class Users(AbstractUser):
    openid = models.CharField(max_length=1000, blank=True, null=True, verbose_name="openid", unique=True)
    info = models.CharField(max_length=1000, blank=True, null=True, verbose_name="info", unique=True)
    nick = models.CharField(max_length=2000, blank=True, null=True, verbose_name="nick", unique=True)
    avatar = models.CharField(max_length=1000, blank=True, null=True, verbose_name="avatar", unique=True)


class AuthView(View):
    def dispatch(self, request, *args, **kwargs):
        # 判断是否有授权
        if not 'user' in request.session:
            # 用户需要访问的url路径
            path = request.get_full_path()

            # 跳转url,
            red_url = '%s?path=%s' % (reverse('wx_auth'), urllib.quote(path))
            return redirect(red_url)

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('nick', 'openid', 'avatar', 'info')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
