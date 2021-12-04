# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class FriendCorp(models.Model):
    name = models.CharField(max_length=100, blank=True)
    corp_url = models.CharField(max_length=100)
    logo = models.FileField(upload_to='corps', blank=True)
    qr_code = models.FileField(upload_to='corps', blank=True)

    class Meta:
        verbose_name = "合作地产公司"
        verbose_name_plural = "合作地产公司"


class MessageCenter(models.Model):
    msg_type = models.CharField(max_length=100, blank=True)
    mls = models.CharField(max_length=100, blank=True)
    agentid = models.CharField(max_length=100, blank=True)
    user_name = models.CharField(max_length=100, blank=True)
    user_tel = models.CharField(max_length=100, blank=True)
    user_email = models.CharField(max_length=100, blank=True)
    user_msg = models.CharField(max_length=1000, blank=True)
    user_ip = models.CharField(max_length=100, blank=True)
    src_url = models.CharField(max_length=1000, blank=True)
    datadate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "消息留言中心"
        verbose_name_plural = "消息留言中心"
