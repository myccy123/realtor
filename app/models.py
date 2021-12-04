# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Listing(models.Model):
    listingid = models.CharField(primary_key = True,max_length=50)
    listingname = models.CharField(max_length=100)
    cityname = models.CharField(max_length=100,db_index=True)
    price = models.CharField(max_length=100)
    areas = models.CharField(max_length=100)
    bedroom = models.CharField(max_length=100)
    toilet = models.CharField(max_length=100)
    parking = models.CharField(max_length=100)
    tax = models.CharField(max_length=100)
    housetype = models.CharField(max_length=100)
    housestyle = models.CharField(max_length=100)
    basement = models.CharField(max_length=100)
    builddate = models.CharField(max_length=100)
    intro = models.TextField()
    goodat = models.TextField()
    corp = models.CharField(max_length=500)
    warning = models.TextField()
    url = models.CharField(max_length=300)
    intro_eng = models.TextField(blank=True,default = '')
    datadate = models.DateTimeField(auto_now_add=True,db_index=True)
    schoolid = models.CharField(max_length=100,blank = True)
    good = models.IntegerField(default = 0)
    visit = models.IntegerField(default = 0)
    postid = models.CharField(max_length=30,blank = True)
    lat = models.CharField(max_length=30,blank = True)
    lng = models.CharField(max_length=30,blank = True)
    
    class Meta:
        verbose_name = '在售房源'
        verbose_name_plural = '在售房源'

class Listing2(models.Model):
    listingid = models.CharField(primary_key = True,max_length=50,blank = True)
    listingname = models.CharField(max_length=100,blank = True)
    cityname = models.CharField(max_length=100,blank = True)
    address = models.CharField(max_length=200,blank = True)
    proaddress = models.CharField(max_length=200,blank = True)
    price1 = models.CharField(max_length=100,blank = True)
    price2 = models.CharField(max_length=100,blank = True)
    areas = models.CharField(max_length=100,blank = True)
    postid = models.CharField(max_length=100,blank = True)
    housetype = models.CharField(max_length=100,blank = True)
    intro = models.TextField(blank = True)
    corp = models.CharField(max_length=500,blank = True)
    warning = models.TextField(blank = True)
    url = models.CharField(max_length=300,blank = True)
    opendate = models.CharField(max_length=300,blank = True)
    sd = models.CharField(max_length=300,blank = True)
    unitnum = models.CharField(max_length=30,blank = True)
    datadate = models.DateTimeField(auto_now_add=True)
    good = models.IntegerField(default = 0)
    visit = models.IntegerField(default = 0)
    
class Userinfo(models.Model):
    userid = models.CharField(max_length=100)
    username = models.CharField(max_length=100,blank = True)
    usercity = models.CharField(max_length=100,blank = True)
    agentid = models.CharField(max_length=100,blank = True)
    creaid = models.CharField(max_length=100,blank = True)
    tel = models.CharField(max_length=100,blank = True)
    note = models.CharField(max_length=100,blank = True)
    email = models.CharField(max_length=100,blank = True)
    siteurl = models.CharField(max_length=100,blank = True)
    assistant = models.CharField(max_length=100,blank = True)
    assistanttel = models.CharField(max_length=100,blank = True)
    address = models.CharField(max_length=100,blank = True)
    selfintro = models.TextField(blank = True)
    teamintro = models.TextField(blank = True)
    corpintro = models.TextField(blank = True)
    warning = models.TextField(blank = True)
    corp = models.CharField(max_length=100,blank = True)
    bal = models.DecimalField(max_digits=16,decimal_places=2,default = 0)
    role = models.CharField(max_length=20,blank = True)
    creditcard = models.CharField(max_length=20,blank = True)
    enddt = models.CharField(max_length=20,blank = True)
    cvs = models.CharField(max_length=20,blank = True)
    postid = models.CharField(max_length=20,blank = True)
    wechatid = models.CharField(max_length=100,blank = True)
    visit = models.IntegerField(default = 0)
    good = models.IntegerField(default = 0)

class Userimage(models.Model):
    userid = models.CharField(max_length=100)
    imgtype = models.CharField(max_length=10)
    img = models.FileField(upload_to='userimgs')
    
class Listingimg(models.Model):
    imgname = models.CharField(primary_key = True,max_length=50,blank = True)
    listingid = models.CharField(max_length=50,db_index=True)
    img = models.FileField(upload_to='listings')
    imgtype = models.CharField(max_length=50,blank = True)

class Article(models.Model):
    article_id = models.CharField(primary_key = True,max_length=50,blank = True)
    article_type = models.CharField(max_length=50,blank = True,db_index = True)
    title = models.CharField(max_length=200,blank = True)
    pro = models.CharField(max_length=2000,blank = True)
    img_url = models.CharField(max_length=200,blank = True)
    article_url = models.CharField(max_length=200,blank = True)
    eng_title = models.CharField(max_length=200,blank = True,default = '')
    datadate = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = '热点文章'
        verbose_name_plural = '热点文章'
 
class Template(models.Model):
    tempid = models.CharField(max_length=100)
    userid = models.CharField(max_length=100)
    temptype = models.CharField(max_length=100)
    temp = models.CharField(max_length=100)
    savetime = models.DateTimeField(auto_now_add=True)

class Freeedit(models.Model):
    dataid = models.CharField(max_length=100)
    userid = models.CharField(max_length=100)
    title = models.CharField(max_length=100,default = '我的瑞安居')
    note = models.CharField(max_length=5000,blank = True)
    img = models.FileField(upload_to='freeedit',blank = True)
 
class Sharesite(models.Model):
    htmlid = models.CharField(max_length=100)
    tempid = models.CharField(max_length=100,blank = True)
    userid = models.CharField(max_length=100)
    dataid = models.CharField(max_length=100,blank = True)
    sharetype = models.CharField(max_length=30,blank = True)
    sharetime = models.DateTimeField(auto_now_add=True,blank = True)
    url = models.CharField(max_length=100,blank = True)
    good = models.IntegerField(default = 0)
    visit = models.IntegerField(default = 0)
    comm = models.IntegerField(default = 0)
    translated = models.CharField(max_length=1,default = '0')
    shared = models.CharField(max_length=1,default = '0')
    temp = models.CharField(max_length=100,blank = True)
    labels = models.CharField(max_length=100,blank = True)

class Sitecomment(models.Model):
    htmlid = models.CharField(max_length=100)
    commtime = models.DateTimeField(auto_now_add=True)
    commtype = models.CharField(max_length=100,blank = True)
    userid = models.CharField(max_length=100,blank = True)
    usercomment = models.CharField(max_length=500,blank = True)

class Systemorder(models.Model):
    STATUS_CHOICES = (('pending','待处理'),('completed','正在推广'),('shared','已结束'),('commented','已评价'))
    htmlid = models.CharField(max_length=100)
    userid = models.CharField(max_length=100)
    dataid = models.CharField(max_length=100,blank = True)
    ordertype = models.CharField(max_length=100,blank = True)
    starttime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)
    transid = models.CharField(max_length=100,blank = True)
    
    class Meta:
        verbose_name = '系统订单'
        verbose_name_plural = '系统订单'
    
class Advertisement(models.Model):
    STATUS_CHOICES = (('fx','发现页广告'),
                      ('dz','私人订制页广告'),
                      ('atc1','文章列表页广告(大)'),
                      ('atc2','文章列表页广告(小)'),
                      ('yz','验证页广告'),
                      ('hy','进入APP欢迎页'),
                      )
    img = models.FileField(upload_to='ad')
    url = models.CharField(max_length=100,blank = True)
    active = models.CharField(max_length=1,default = '1')
    adtype = models.CharField(max_length=20,choices=STATUS_CHOICES)
    
    class Meta:
        verbose_name = '广告'
        verbose_name_plural = '广告'
 
class Coupon(models.Model):
    couponid = models.AutoField(primary_key=True)
    coupontype = models.CharField(max_length=100)
    userid = models.CharField(max_length=100)
    htmlid = models.CharField(max_length=100,blank = True)
    condi = models.CharField(max_length=100,blank = True)
    amt = models.DecimalField(max_digits=16,decimal_places=2,default = 0)
    startdt = models.DateTimeField(auto_now_add=True)
    enddt = models.DateTimeField(blank = True)
    usable = models.CharField(max_length=1)
    couponname = models.CharField(max_length=100,blank = True)

class Discount(models.Model):
    beginamt = models.IntegerField()
    endamt = models.IntegerField()
    percent = models.DecimalField(max_digits=16,decimal_places=2,default = 0)
 
class Custom(models.Model):
    cityname = models.CharField(max_length=100,blank=True)
    bedroom = models.CharField(max_length=100,blank=True)
    toilet = models.CharField(max_length=100,blank=True)
    userid = models.CharField(max_length=100,blank=True)
    username = models.CharField(max_length=100,blank=True)
    usercity = models.CharField(max_length=100,blank=True)
    tel = models.CharField(max_length=100,blank=True)
    pricezone = models.CharField(max_length=100,blank=True)
    buydate = models.CharField(max_length=100,blank=True)
    addservice = models.CharField(max_length=100,blank=True)
    datadate = models.DateTimeField(auto_now_add=True)
    housetype = models.CharField(max_length=100,blank=True)
    notes = models.CharField(max_length=3000,blank=True)
    
    class Meta:
        verbose_name = '私人订制'
        verbose_name_plural = '私人订制'
 
class Feedback(models.Model):
    userid = models.CharField(max_length=100,blank=True)
    problem = models.CharField(max_length=2000,blank=True)
    idea = models.CharField(max_length=2000,blank=True)
    tel = models.CharField(max_length=100,blank=True)
    email = models.CharField(max_length=100,blank=True)
    datadate = models.DateTimeField(auto_now_add=True)
    img1 = models.FileField(upload_to='feedback',default='')
    img2 = models.FileField(upload_to='feedback',default='')
    img3 = models.FileField(upload_to='feedback',default='')
    
    class Meta:
        verbose_name = '问题反馈'
        verbose_name_plural = '问题反馈'

class Telcode(models.Model):
    tel = models.CharField(max_length=100)
    vcode = models.CharField(max_length=6)

class Access_hitory(models.Model):
    addr = models.CharField(max_length=100,blank = True)
    actiontype = models.CharField(max_length=20,blank = True)
    htmlid = models.CharField(max_length=100,blank = True)
    htmltype = models.CharField(max_length=100,blank = True)
    userid = models.CharField(max_length=100,blank = True)
    datadate = models.DateTimeField(auto_now_add=True)
    agent = models.CharField(max_length=1000,blank = True)
    referer = models.CharField(max_length=5000,blank = True)
    sess = models.CharField(max_length=1000,blank = True)

class Wechat_info(models.Model):
    unionid = models.CharField(max_length=100,blank = True)
    openid = models.CharField(max_length=100,blank = True)
    nickname = models.CharField(max_length=100,blank = True)
    sex = models.CharField(max_length=100,blank = True)
    province = models.CharField(max_length=100,blank = True)
    city = models.CharField(max_length=100,blank = True)
    country = models.CharField(max_length=100,blank = True)
    headimgurl = models.CharField(max_length=900,blank = True)
    privilege = models.CharField(max_length=100,blank = True)
    datadate = models.DateTimeField(auto_now_add=True)

class Charge_history(models.Model):
    userid = models.CharField(max_length=100,blank = True)
    cardid = models.CharField(max_length=100,blank = True)
    cvs = models.CharField(max_length=10,blank = True)
    enddt = models.CharField(max_length=30,blank = True)
    curr = models.CharField(max_length=3,blank = True)
    amt = models.DecimalField(max_digits=16,decimal_places=2,default = 0)
    tax = models.DecimalField(max_digits=16,decimal_places=2,default = 0)
    discount = models.DecimalField(max_digits=16,decimal_places=2,default = 0)
    invoiced = models.CharField(max_length=1,blank = True)
    datadate = models.DateTimeField(auto_now_add=True)

class Invoiced_history(models.Model):
    chargeids = models.CharField(max_length=1000,blank = True)
    userid = models.CharField(max_length=100,blank = True)
    email = models.CharField(max_length=100,blank = True)
    addr = models.CharField(max_length=1000,blank = True)
    postid = models.CharField(max_length=100,blank = True)
    datadate = models.DateTimeField(auto_now_add=True)

class System_msg(models.Model):
    STATUS_CHOICES = (('pending','待发送'),('sended','已发送'))
    userid = models.CharField(max_length=100,blank = True)
    msgtype = models.CharField(max_length=20,default = 'text')
    msgstatus = models.CharField(max_length=20,choices=STATUS_CHOICES)
    target = models.CharField(max_length=5000,blank = True)
    msgtitle = models.CharField(max_length=200,blank = True)
    msg = models.CharField(max_length=5000,blank = True)
    datadate = models.DateTimeField(auto_now=True)
    createdate = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '系统通知'
        verbose_name_plural = '系统通知'

class Publish_apk(models.Model):
    versioncode = models.CharField(max_length=10,blank = True)
    versionName = models.CharField(max_length=100,blank = True)
    apkname = models.CharField(max_length=100,blank = True)
    apkinfo = models.CharField(max_length=2000,blank = True)
    apk = models.FileField(upload_to='apks',default='')
    datadate = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '应用更新'
        verbose_name_plural = '应用更新'

class School_dist(models.Model):
    schoolid = models.CharField(max_length=100,blank = True)
    schoolname = models.CharField(max_length=100,blank = True)
    schoolcity = models.CharField(max_length=100,blank = True)
    schooltype = models.CharField(max_length=100,blank = True)
    rank1 = models.CharField(max_length=100,blank = True)
    rank2 = models.CharField(max_length=100,blank = True)
    parentsin = models.CharField(max_length=100,blank = True)
    testnum = models.CharField(max_length=100,blank = True)
    noneng = models.CharField(max_length=100,blank = True)
    fran = models.CharField(max_length=100,blank = True)
    spec = models.CharField(max_length=100,blank = True)
    tel = models.CharField(max_length=100,blank = True)
    studentnum = models.CharField(max_length=100,blank = True)
    schooladdr = models.CharField(max_length=100,blank = True)
    registnum = models.CharField(max_length=100,blank = True)
    schoolhead = models.CharField(max_length=100,blank = True)
    fax = models.CharField(max_length=100,blank = True)
    datadate = models.DateTimeField(auto_now_add=True)

