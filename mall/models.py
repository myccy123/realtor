# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Wechat_user_info(models.Model):
    openid = models.CharField(max_length=50)
    nickname = models.CharField(max_length=100,blank = True)
    headimgurl = models.CharField(max_length=1000,blank = True)
    sex = models.CharField(max_length=100,blank = True)
    city = models.CharField(max_length=100,blank = True)
    province = models.CharField(max_length=100,blank = True)
    country = models.CharField(max_length=100,blank = True)
    language = models.CharField(max_length=100,blank = True)
    logindate = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = '微信用户信息'
        verbose_name_plural = '微信用户信息'

class Product_info(models.Model):
    product_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=100,blank = True)
    product_title = models.CharField(max_length=1000,blank = True)
    product_desc = models.CharField(max_length=1000,blank = True)
    price = models.CharField(max_length=100,blank = True)
    product_img = models.FileField(upload_to='product_imgs',blank = True)
    createdate = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = '商品信息表'
        verbose_name_plural = '商品信息表'

class Product_sets(models.Model):
    set_id = models.CharField(max_length=100,blank = True)
    product_id = models.CharField(max_length=50)
    set_name = models.CharField(max_length=1000,blank = True)
    set_price = models.CharField(max_length=1000,blank = True)
    createdate = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = '商品套餐表'
        verbose_name_plural = '商品套餐表'
        
class Product_detail(models.Model):
    STATUS_CHOICES = (('txt','文字'),
                      ('img','图片'),
                      )
    product_id = models.CharField(max_length=50)
    orderid = models.IntegerField()
    detail_type = models.CharField(max_length=500,default = 'txt',choices=STATUS_CHOICES)
    product_text = models.CharField(max_length=1000,blank = True)
    product_img = models.FileField(upload_to='product_imgs',blank = True)
    class Meta:
        verbose_name = '商品详情表'
        verbose_name_plural = '商品详情表'

class Orders(models.Model):
    set_id = models.CharField(max_length=100,blank = True)
    product_id = models.CharField(max_length=50)
    set_price = models.CharField(max_length=1000,blank = True)
    userid = models.CharField(max_length=50)
    tel = models.CharField(max_length=50)
    addr = models.CharField(max_length=1000,blank = True)
    order_status = models.CharField(max_length=50)
    createdate = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = '订单表'
        verbose_name_plural = '订单表'
        
class Address_book(models.Model):
    addrid = models.CharField(max_length=50,blank = True)
    userid = models.CharField(max_length=50,blank = True)
    recvname = models.CharField(max_length=50,blank = True)
    recvtel = models.CharField(max_length=50,blank = True)
    addr = models.CharField(max_length=1000,blank = True)
    addr_type = models.CharField(max_length=50,blank = True)
    createdate = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = '地址表'
        verbose_name_plural = '地址表'

