# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class agent_info(models.Model):
    STATUS_CHOICES = (('1', '是'),
                      ('0', '否'),
                      )
    STATUS_CHOICES2 = (('weekly', '每周发送'),
                       ('pause', '暂停发送'),
                       )

    userid = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    note = models.CharField(max_length=100, blank=True)
    agenttype = models.CharField(max_length=10, blank=True)
    website = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    selfintro = models.TextField(blank=True)
    selfintro_cn = models.TextField(blank=True)
    corpintro = models.TextField(blank=True)
    corpintro_cn = models.TextField(blank=True)
    teamintro = models.TextField(blank=True)
    teamintro_cn = models.TextField(blank=True)
    corp = models.CharField(max_length=100, blank=True)
    postid = models.CharField(max_length=20, blank=True)
    head = models.FileField(upload_to='agentimgs', blank=True)
    qrcode = models.FileField(upload_to='agentimgs', blank=True)
    logo = models.FileField(upload_to='agentimgs', blank=True)
    username2 = models.CharField(max_length=100, blank=True)
    tel2 = models.CharField(max_length=100, blank=True)
    email2 = models.CharField(max_length=100, blank=True)
    head2 = models.FileField(upload_to='agentimgs', blank=True)
    qrcode2 = models.FileField(upload_to='agentimgs', blank=True)
    country = models.CharField(max_length=100, blank=True)
    prov = models.CharField(max_length=100, blank=True)
    group = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    datadate = models.DateTimeField(auto_now=True)
    fname = models.CharField(max_length=100, blank=True)
    lname = models.CharField(max_length=100, blank=True)
    active = models.CharField(max_length=10, default='1',
                              choices=STATUS_CHOICES)
    emailscd = models.CharField(max_length=10, default='weekly',
                                choices=STATUS_CHOICES2)

    class Meta:
        verbose_name = "经纪用户信息表"
        verbose_name_plural = "经纪用户信息表"


class agent_img(models.Model):
    IMG_TYPE_CHOICES = (('agent', '经纪照片'),
                        ('corp', '公司照片'),
                        ('video', '经纪视频'),
                        ('emaillist', '邮件列表（Excel）'),
                        )

    userid = models.CharField(max_length=100)
    imgtype = models.CharField(max_length=100, blank=True,
                               choices=IMG_TYPE_CHOICES)
    img = models.FileField(upload_to='agentimgs', blank=True)

    class Meta:
        verbose_name = "经纪图片"
        verbose_name_plural = "经纪图片"


class agent_auth(models.Model):
    STATUS_CHOICES = (('paid', '已支付'),
                      ('not paid', '未支付'),
                      )

    SERVICE_CHOICES = (('vip', '会员服务 ($288/年)'),
                       ('auth', '翻译及认证服务费 ($79)'),
                       ('sp', 'Smartflyer ($99/Listing)'),
                       ('subscription', '2020 Subscription Package'),
                       ('domain', '经纪主页域名 ($20)'),
                       ('engagement', '买家吸引套餐 ($360)'),
                       ('diyPage', '经纪人页面样式跳转,可配置不同的CSS和HTML样式($499/year)'),
                       )

    userid = models.CharField(max_length=100)
    bgndate = models.DateTimeField(null=True)
    enddate = models.DateTimeField(null=True)
    fee = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    service = models.CharField(max_length=100, default='vip',
                               choices=SERVICE_CHOICES)
    status = models.CharField(max_length=10, default='not paid',
                              choices=STATUS_CHOICES)
    cardno = models.CharField(max_length=30, blank=True)
    token = models.CharField(max_length=30, blank=True)
    invoice = models.FileField(upload_to='sp_invoice', blank=True)

    class Meta:
        verbose_name = "经纪认证表"
        verbose_name_plural = "经纪认证表"


class agent_card(models.Model):
    STATUS_CHOICES = (('0', '历史信用卡'),
                      ('1', '默认付款卡'),
                      ('deleted', '已删除的卡'),
                      )

    userid = models.CharField(max_length=100)
    holder = models.CharField(max_length=100, blank=True)
    cardno = models.CharField(max_length=100, blank=True)
    expire = models.CharField(max_length=10, blank=True)
    cvs = models.CharField(max_length=3, blank=True)
    postid = models.CharField(max_length=100, blank=True)
    cardtype = models.CharField(max_length=10, default='1',
                                choices=STATUS_CHOICES)

    class Meta:
        verbose_name = "信用卡信息表"
        verbose_name_plural = "信用卡信息表"


class tmp_token(models.Model):
    userid = models.CharField(max_length=100)
    token = models.CharField(max_length=100, blank=True)
    datadate = models.DateTimeField(auto_now=True)


class cust_message(models.Model):
    userid = models.CharField(max_length=100)
    custname = models.CharField(max_length=100, blank=True)
    custemail = models.CharField(max_length=100, blank=True)
    custmsg = models.CharField(max_length=2000, blank=True)
    mls = models.CharField(max_length=100, blank=True)
    msgtype = models.CharField(max_length=100, blank=True)
    datadate = models.DateTimeField(auto_now=True)


class email_list(models.Model):
    userid = models.CharField(max_length=100, blank=True)
    mls = models.CharField(max_length=100, blank=True)
    fname = models.CharField(max_length=100, blank=True)
    lname = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    msg = models.CharField(max_length=1000, blank=True)
    src = models.CharField(max_length=100, blank=True)
    datadate = models.DateTimeField(auto_now_add=True)
