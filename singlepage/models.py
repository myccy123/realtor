# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Listing_for_sp(models.Model):
    STATUS_CHOICES = (('0', '国外经纪'),
                      ('1', '国内经纪'),
                      )
    STATUS_CHOICES3 = (('0', '不推广'),
                       ('1', '推广'),
                       )
    STATUS_CHOICES2 = (('no', 'MLS'),
                       ('yes', '已售'),
                       ('rent', '出租'),
                       ('rented', '已租'),
                       ('presale', '楼花'),
                       ('dark', '暗盘'),
                       ('invalid', '未升效'),
                       )
    DIST_CHOICES = (
        ('WestVan', '西温哥华'),
        ('VancouverWest', '温哥华西区'),
        ('Vancouvereast', '温哥华东区'),
        ('NorthVancouver', '北温'),
        ('Burnaby', '本拿比'),
        ('whiterock', '白石'),
        ('Surrey', '素里'),
        ('Richmond', '列治文'),
        ('Coquitlam', '高贵林'),
        ('newWestminster', '新西敏'),
        ('Chilliwack', '奇利瓦克'),
        ('delta', '三角洲'),
        ('Langley', '兰里'),
        ('Mission', '米逊'),
        ('abbotsford', '阿伯茨福德'),
        ('NorthSurrey', '北素里'),
        ('Hope', '霍普'),
        ('Cultus', '卡尔特斯'),
        ('Rosedale', '玫瑰谷'),
        ('squimish', '斯阔米什'),
        ('PortMoody', '满地宝'),
        ('SunshineCoast', '阳光海岸'),
        ('MapleRidge', '枫树岭'),
        ('Whistler', '惠斯勒'),
        ('Pemberton', '彭伯顿'),
        ('Ladner', '拉德纳'),
        ('Cloverdale', '克洛弗代尔'),
        ('Tsawwassen', '措瓦森'),
        ('Bowen', '宝云岛'),
        ('PortCoquitlam', '高贵林港'),
        ('Sardis', '萨迪斯'),
        ('PittMeadows', '匹特草原'),
        ('Harrison', '哈里森'),
        ('Agassiz', '阿加西'),
        ('Yarrow', '亚罗'),
    )

    listingid = models.CharField(max_length=50, blank=True)
    listingname = models.CharField(max_length=100, blank=True)
    cityname = models.CharField(max_length=100, db_index=True, blank=True)
    price = models.CharField(max_length=100, blank=True)
    areas = models.CharField(max_length=100, blank=True)
    bedroom = models.CharField(max_length=100, blank=True)
    toilet = models.CharField(max_length=100, blank=True)
    parking = models.CharField(max_length=100, blank=True)
    tax = models.CharField(max_length=100, blank=True)
    housetype = models.CharField(max_length=100, blank=True)
    housestyle = models.CharField(max_length=100, blank=True)
    basement = models.CharField(max_length=100, blank=True)
    builddate = models.CharField(max_length=100, blank=True)
    intro = models.TextField(blank=True)
    goodat = models.TextField(blank=True)
    corp = models.CharField(max_length=500, blank=True)
    warning = models.TextField(blank=True)
    intro_zh = models.TextField(blank=True, default='')
    datadate = models.DateTimeField(auto_now_add=True)
    schoolid = models.CharField(max_length=100, blank=True)
    good = models.IntegerField(default=0)
    visit = models.IntegerField(default=0)
    postid = models.CharField(max_length=30, blank=True)
    lat = models.CharField(max_length=30, blank=True)
    lng = models.CharField(max_length=30, blank=True)
    token = models.CharField(max_length=100, blank=True)
    vrtour = models.TextField(blank=True)
    titleagent = models.CharField(max_length=1, default='0',
                                  choices=STATUS_CHOICES)
    salestatus = models.CharField(max_length=30, default='invalid',
                                  choices=STATUS_CHOICES2)
    url = models.CharField(max_length=5000, blank=True)
    othermls = models.CharField(max_length=500, blank=True)
    listingtype = models.CharField(max_length=500, blank=True, default='特色房源')
    lastdate = models.DateTimeField(auto_now=True)
    distid = models.CharField(max_length=50, blank=True, choices=DIST_CHOICES)
    sptype = models.CharField(max_length=100, blank=True, default='smf')
    isspread = models.CharField(max_length=10, blank=True, default='0',
                                choices=STATUS_CHOICES3)
    mapspread = models.CharField(max_length=10, blank=True, default='0',
                                choices=STATUS_CHOICES3)

    class Meta:
        verbose_name = '在售房源'
        verbose_name_plural = '在售房源'


class Open_house(models.Model):
    listingid = models.CharField(max_length=50)
    date1 = models.CharField(max_length=100, blank=True)
    time1 = models.CharField(max_length=100, blank=True)
    date2 = models.CharField(max_length=100, blank=True)
    time2 = models.CharField(max_length=100, blank=True)
    date3 = models.CharField(max_length=100, blank=True)
    time3 = models.CharField(max_length=100, blank=True)
    date4 = models.CharField(max_length=100, blank=True)
    time4 = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = '公众开放日'
        verbose_name_plural = '公众开放日'


class Openhouse(models.Model):
    listingid = models.CharField(max_length=50)
    bgndate1 = models.DateTimeField(null=True, blank=True)
    enddate1 = models.DateTimeField(null=True, blank=True)
    bgndate2 = models.DateTimeField(null=True, blank=True)
    enddate2 = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = '公众开放日'
        verbose_name_plural = '公众开放日'


class Tokens(models.Model):
    token = models.CharField(max_length=100)
    userid = models.CharField(max_length=100, blank=True)
    tokentype = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)
    active = models.CharField(max_length=1)


class Call_history(models.Model):
    listingid = models.CharField(max_length=30)
    agentid = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=30)
    tel = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    ip = models.CharField(max_length=20, blank=True)
    datadate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '用户留言信息'
        verbose_name_plural = '用户留言信息'


class User_information(models.Model):
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=50, blank=True)
    tel = models.CharField(max_length=30, blank=True)
    website = models.CharField(max_length=1000, blank=True)
    introduction = models.CharField(max_length=5000, blank=True)
    head = models.FileField(upload_to='sp_users', blank=True)
    logo = models.FileField(upload_to='sp_users', blank=True)
    cn_username = models.CharField(max_length=50, blank=True)
    cn_tel = models.CharField(max_length=50, blank=True)
    cn_email = models.CharField(max_length=100, blank=True)
    cn_head = models.FileField(upload_to='sp_users', blank=True)
    cn_QR = models.FileField(upload_to='sp_users', blank=True)

    class Meta:
        verbose_name = '客户信息'
        verbose_name_plural = '客户信息'


class Sp_img(models.Model):
    STATUS_CHOICES = (('hx', '户型图'),
                      ('video', '视频'),
                      ('pdf', 'PDF'),
                      ('bgimg1', '第一幅背景图'),
                      ('bgimg2', '第二幅背景图'),
                      ('bgimg3', '第三幅背景图'),
                      ('bgimg4', '第四幅背景图'),
                      ('preimg', '缩略图'),
                      )

    listingid = models.CharField(max_length=50)
    imgtype = models.CharField(max_length=100, choices=STATUS_CHOICES)
    img = models.FileField(upload_to='sp_imgs', blank=True)
    owner = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = '房源图片及视频'
        verbose_name_plural = '房源图片及视频'


class Flow_statistics(models.Model):
    addr = models.CharField(max_length=100, blank=True)
    htmlid = models.CharField(max_length=1000, blank=True)
    htmltype = models.CharField(max_length=10, blank=True)
    userid = models.CharField(max_length=100, blank=True)
    datadate = models.DateTimeField(auto_now_add=True)
    agent = models.CharField(max_length=1000, blank=True)
    referer = models.CharField(max_length=1000, blank=True)
    sess = models.CharField(max_length=1000, blank=True)


class Order_from_website(models.Model):
    fname = models.CharField(max_length=100, blank=True)
    lname = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    mls = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=100, blank=True)
    corp = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    postid = models.CharField(max_length=100, blank=True)


class BI_map(models.Model):
    mls = models.CharField(max_length=20, blank=True)
    token = models.CharField(max_length=50, blank=True)
    template_id = models.CharField(max_length=50, blank=True)
    orderid = models.IntegerField(default=0)


class finance(models.Model):
    STATUS_CHOICES = (('paid', '已支付'),
                      ('not paid', '未支付'),
                      ('ubertor', 'Uberotr支付'),
                      )

    mls = models.CharField(max_length=20, blank=True)
    token = models.CharField(max_length=50, blank=True)
    userid = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=100, blank=True)
    cardid = models.CharField(max_length=50, blank=True)
    yyyy = models.CharField(max_length=4, blank=True)
    mm = models.CharField(max_length=2, blank=True)
    cvs = models.CharField(max_length=10, blank=True)
    invoice = models.FileField(upload_to='sp_invoice', blank=True)
    status = models.CharField(max_length=50, default='not paid',
                              choices=STATUS_CHOICES)

    class Meta:
        verbose_name = '发票、信用卡信息'
        verbose_name_plural = '发票、信用卡信息'


class card_update_record(models.Model):
    mls = models.CharField(max_length=20, blank=True)
    token = models.CharField(max_length=50, blank=True)
    userid = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=100, blank=True)
    cardid = models.CharField(max_length=50, blank=True)
    yyyy = models.CharField(max_length=4, blank=True)
    mm = models.CharField(max_length=2, blank=True)
    cvs = models.CharField(max_length=10, blank=True)
    lastdate = models.DateTimeField(auto_now=True)
