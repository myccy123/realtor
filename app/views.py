# -*- coding:utf-8 -*-
from app.models import *
from forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.db.models import Q
import json
import random
import uuid
import re
import datetime
import os
from myweb.itools import *

def get_res_info(code = '0',msg = 'ok'):
    res = {}
    res['rescode'] = code
    res['resmsg'] = msg
    return json.dumps(res,indent = 2,ensure_ascii=False)

def make_rcmd_info(obj,otype,request):
    jsn = {}
    if otype == 'school':
        jsn['img'] = 'http://' + request.META['HTTP_HOST'] + '/static/img/icon_school_%s.png' % str(random.randint(0, 5))
        imgs = Listingimg.objects.filter(listingid=obj.schoolid,imgtype='school')
        for img in imgs:
            jsn['img'] = img.img.url
        jsn['schoolid'] = obj.schoolid
        jsn['schoolname'] = obj.schoolname
        jsn['schoolcity'] = obj.schoolcity
        jsn['schooltype'] = obj.schooltype
        jsn['rank1'] = obj.rank1
        jsn['rank2'] = obj.rank2
        jsn['parentsin'] = obj.parentsin
        jsn['testnum'] = obj.testnum
        jsn['noneng'] = obj.noneng
        jsn['fran'] = obj.fran
        jsn['spec'] = obj.spec
        jsn['tel'] = obj.tel
        jsn['studentnum'] = obj.studentnum
        jsn['schooladdr'] = obj.schooladdr
        jsn['registnum'] = obj.registnum
        jsn['schoolhead'] = obj.schoolhead
        jsn['fax'] = obj.fax
        jsn['datadate'] = obj.datadate.strftime('%Y-%m-%d')
    elif otype == 'listing':
        obj.visit += 1
        obj.save()
        imgs = Listingimg.objects.filter(listingid = obj.listingid)
        imgurl = []
        jsn['map'] = ''
        jsn['mp4'] = ''
        for img in imgs:
            if img.imgtype == 'listing1':
                imgurl.append(img.img.url)
            elif img.imgtype == 'map':
                jsn['map'] = img.img.url
            elif img.imgtype == 'mp4':
                jsn['mp4'] = img.img.url
        jsn['imgurl'] = imgurl if len(imgurl) > 0 else ['http://www.realtoraccess.com/static/img/def_listingimg%s.jpg' % str(random.randint(1, 5))]
        jsn['listingid'] = obj.listingid
        jsn['listingname'] = obj.listingname
        jsn['cityname'] = get_code('t99_cityname', obj.cityname)
        jsn['price'] = obj.price
        jsn['areas'] = obj.areas
        jsn['bedroom'] = obj.bedroom
        jsn['toilet'] = obj.toilet
        jsn['parking'] = obj.parking
        jsn['tax'] = obj.tax
        jsn['housetype'] = obj.housetype
        jsn['housestyle'] = obj.housestyle
        jsn['basement'] = obj.basement
        jsn['builddate'] = obj.builddate
        jsn['intro'] = obj.intro
        jsn['goodat'] = obj.goodat
        jsn['corp'] = obj.corp
        jsn['warning'] = obj.warning
        jsn['intro_eng'] = obj.intro_eng
        jsn['visit'] = obj.visit
        jsn['good'] = obj.good
        jsn['datadate'] = obj.datadate.strftime('%Y-%m-%d')
    return jsn

def make_json(ls):
    jsn = {}
    if ls.sharetype == 'listing1':
        listingid = ls.dataid
        l = Listing.objects.get(listingid = listingid)
        imgs = Listingimg.objects.filter(listingid = listingid)
        u = Userinfo.objects.get(userid = ls.userid)
        uimg = Userimage.objects.get(userid = ls.userid,imgtype = 'head')
        imgurl = []
        jsn['map'] = ''
        jsn['mp4'] = ''
        for img in imgs:
            if img.imgtype == 'listing1':
                imgurl.append(img.img.url)
            elif img.imgtype == 'map':
                jsn['map'] = img.img.url
            elif img.imgtype == 'mp4':
                jsn['mp4'] = img.img.url
        jsn['sharetype'] = ls.sharetype
        jsn['temp'] = ls.temp
        jsn['labels'] = ls.labels
        jsn['listingid'] = l.listingid
        jsn['listingname'] = l.listingname
        jsn['cityname'] = get_code('t99_cityname', l.cityname)
        jsn['price'] = l.price
        jsn['areas'] = l.areas
        jsn['bedroom'] = l.bedroom
        jsn['toilet'] = l.toilet
        jsn['parking'] = l.parking
        jsn['tax'] = l.tax
        jsn['housetype'] = l.housetype
        jsn['housestyle'] = l.housestyle
        jsn['basement'] = l.basement
        jsn['builddate'] = l.builddate
        jsn['intro'] = l.intro
        jsn['goodat'] = l.goodat
        jsn['corp'] = l.corp
        jsn['warning'] = l.warning
        jsn['intro_eng'] = l.intro_eng
        jsn['htmlid'] = ls.htmlid
        jsn['url'] = ls.url
        jsn['time'] = ls.sharetime.strftime('%Y-%m-%d')
        jsn['translated'] = ls.translated
        jsn['imgurl'] = imgurl if len(imgurl) > 0 else ['http://www.realtoraccess.com/static/img/def_listingimg%s.jpg' % str(random.randint(1, 5))]
        jsn['userid'] = u.userid
        jsn['username'] = u.username
        jsn['usercity'] = u.usercity
        jsn['userimg'] = uimg.img.url
        jsn['usercorp'] = u.corp
        jsn['useraddr'] = u.address
        jsn['visit'] = Access_hitory.objects.filter(htmlid=ls.htmlid).values('addr').distinct().count()
        jsn['good'] = ls.good
        jsn['comment'] = ls.comm
    elif ls.sharetype == 'listing2':
        listingid = ls.dataid
        l = Listing2.objects.get(listingid = listingid)
        imgs = Listingimg.objects.filter(listingid = listingid)
        u = Userinfo.objects.get(userid = ls.userid)
        uimg = Userimage.objects.get(userid = ls.userid,imgtype = 'head')
        imgurl = []
        huxing = []
        jsn['map'] = ''
        jsn['mp4'] = ''
        for img in imgs:
            if img.imgtype == 'listing2':
                imgurl.append(img.img.url)
            elif img.imgtype == 'map':
                jsn['map'] = img.img.url
            elif img.imgtype == 'mp4':
                jsn['mp4'] = img.img.url
            elif img.imgtype == 'huxing':
                huxing.append(img.img.url)
        jsn['sharetype'] = ls.sharetype
        jsn['temp'] = ls.temp
        jsn['labels'] = ls.labels
        jsn['huxing'] = huxing
        jsn['listingid'] = l.listingid
        jsn['listingname'] = l.listingname
        jsn['cityname'] = l.cityname
        jsn['address'] = l.address
        jsn['areas'] = l.areas
        jsn['postid'] = l.postid
        jsn['housetype'] = l.housetype
        jsn['intro'] = l.intro
        jsn['corp'] = l.corp
        jsn['warning'] = l.warning
        jsn['opendate'] = l.opendate
        jsn['price1'] = l.price1.replace('万元','')
        jsn['price2'] = l.price2.replace('万元','')
        jsn['proaddress'] = l.proaddress
        jsn['htmlid'] = ls.htmlid
        jsn['url'] = ls.url
        jsn['time'] = ls.sharetime.strftime('%Y-%m-%d')
        jsn['translated'] = ls.translated
        jsn['imgurl'] = imgurl
        jsn['userid'] = u.userid
        jsn['username'] = u.username
        jsn['usercity'] = u.usercity
        jsn['userimg'] = uimg.img.url
        jsn['usercorp'] = u.corp
        jsn['useraddr'] = u.address
        jsn['visit'] = Access_hitory.objects.filter(htmlid=ls.htmlid).values('addr').distinct().count()
        jsn['good'] = ls.good
        jsn['comment'] = ls.comm
    elif ls.sharetype == 'mysite':
        uinfo = Userinfo.objects.get(userid = ls.userid)
        uimg = Userimage.objects.filter(userid = ls.userid)
        jsn = {}
        team = []
        history = []
        comment = []
        for i in uimg:
            if i.imgtype == 'ad':
                jsn['ad'] = i.img.url
            elif i.imgtype == 'wechat':
                jsn['wechat'] = i.img.url
            elif i.imgtype == 'head':
                jsn['head'] = i.img.url
            elif i.imgtype == 'mp4':
                jsn['mp4'] = i.img.url
            elif i.imgtype == 'team':
                team.append(i.img.url)
            elif i.imgtype == 'history':
                history.append(i.img.url)
            elif i.imgtype == 'comment':
                comment.append(i.img.url)
        jsn['sharetype'] = ls.sharetype
        jsn['temp'] = ls.temp
        jsn['userid'] = uinfo.userid
        jsn['username'] = uinfo.username
        jsn['usercity'] = uinfo.usercity
        jsn['tel'] = uinfo.tel
        jsn['note'] = uinfo.note
        jsn['email'] = uinfo.email
        jsn['siteurl'] = uinfo.siteurl
        jsn['assistant'] = uinfo.assistant
        jsn['address'] = uinfo.address
        jsn['selfintro'] = uinfo.selfintro
        jsn['teamintro'] = uinfo.teamintro
        jsn['corpintro'] = uinfo.corpintro
        jsn['warning'] = uinfo.warning
        jsn['agentid'] = uinfo.agentid
        jsn['assistanttel'] = uinfo.assistanttel
        jsn['corp'] = uinfo.corp
        jsn['creaid'] = uinfo.creaid
        jsn['postid'] = uinfo.postid
        jsn['team'] = team
        jsn['history'] = history
        jsn['commurl'] = comment
        jsn['htmlid'] = ls.htmlid
        jsn['time'] = ls.sharetime.strftime('%Y-%m-%d')
        jsn['translated'] = ls.translated
        jsn['url'] = ls.url
        jsn['visit'] = Access_hitory.objects.filter(userid=ls.userid,htmltype='mysite')\
        .values('addr').distinct().count()
        jsn['good'] = ls.good
        jsn['comment'] = ls.comm
    elif ls.sharetype == 'article':
        uinfo = Userinfo.objects.get(userid = ls.userid)
        uimg = Userimage.objects.filter(userid = ls.userid)
        atc = Article.objects.get(article_id = ls.dataid)
        jsn = {}
        for i in uimg:
            if i.imgtype == 'ad':
                jsn['ad'] = i.img.url
            elif i.imgtype == 'wechat':
                jsn['wechat'] = i.img.url
            elif i.imgtype == 'mp4':
                jsn['mp4'] = i.img.url
            elif i.imgtype == 'head':
                jsn['head'] = i.img.url
        jsn['sharetype'] = ls.sharetype
        jsn['temp'] = ls.temp
        jsn['article_id'] = atc.article_id
        jsn['article_type'] = atc.article_type
        jsn['article_type_cn'] = get_code('t99_articletype', atc.article_type)
        jsn['title'] = atc.title
        jsn['pro'] = atc.pro
        jsn['img_url'] = atc.img_url
        jsn['article_url'] = atc.article_url
        jsn['eng_title'] = atc.eng_title
        jsn['datatime'] = atc.datadate.strftime('%Y-%m-%d')
        jsn['userid'] = uinfo.userid
        jsn['username'] = uinfo.username
        jsn['usercity'] = uinfo.usercity
        jsn['tel'] = uinfo.tel
        jsn['note'] = uinfo.note
        jsn['email'] = uinfo.email
        jsn['siteurl'] = uinfo.siteurl
        jsn['assistant'] = uinfo.assistant
        jsn['assistanttel'] = uinfo.assistanttel
        jsn['corp'] = uinfo.corp
        jsn['useraddr'] = uinfo.address
        jsn['htmlid'] = ls.htmlid
        jsn['time'] = ls.sharetime.strftime('%Y-%m-%d')
        jsn['translated'] = ls.translated
        jsn['url'] = ls.url
        jsn['visit'] = Access_hitory.objects.filter(htmlid=ls.htmlid).values('addr').distinct().count()
        jsn['good'] = ls.good
        jsn['comment'] = ls.comm
    return jsn

def signup1(request):
    form = Signup1(request.POST)
    if form.is_valid():
        fname = form.cleaned_data['fname']
        sname = form.cleaned_data['sname']
        city = form.cleaned_data['city']
        userid = form.cleaned_data['userid']
        passwd1 = form.cleaned_data['passwd1']
        passwd2 = form.cleaned_data['passwd2']
        if passwd1 <> passwd2:
            return HttpResponse(get_res_info('1','passwd err'))
        if User.objects.all().filter(username = userid):
            return HttpResponse(get_res_info('2','user already exist'))
        u = User.objects.create_user(userid,userid,passwd1)
        u.first_name = fname
        u.last_name = sname
        u.save()
        ui = Userinfo(userid = userid,username = fname+' '+sname,email = userid,usercity = city,role='agent')
        ui.save()
        t1 = Template(tempid = '',userid = userid,temptype = 'listing1',temp = 'a1b1c1d1e1f1g1h1i1j1k0l0')
        t2 = Template(tempid = '',userid = userid,temptype = 'listing2',temp = 'a1b1c1d1e1f1g1h1i1j1k1l1m0')
        t3 = Template(tempid = '',userid = userid,temptype = 'mysite',temp = 'a1b1c1d1e1f1g1h1i1j1k1l1m0n1')
        t4 = Template(tempid = '',userid = userid,temptype = 'article',temp = 'a1b1c1d1e1f1g1h0')
        t1.save()
        t2.save()
        t3.save()
        t4.save()
        uimg = Userimage(userid=userid,imgtype='head',img='userimgs/defhead.png')
        uimg.save()
        uimg = Userimage(userid=userid,imgtype='ad',img='userimgs/defad.png')
        uimg.save()
        hx = signup_hx(str(ui.id))
        if hx == 'ok':
            #send_welcome(userid)
            return HttpResponse(get_res_info())
        else:
            return HttpResponse(get_res_info('1','huanxin signup err'))
    else:
        err = ''
        for e in form.errors:
            err = err+e+'->'+form.errors[e]+'|||'
        return HttpResponse(err)

def signup2(request):
    form = Signup2(request.POST)
    if form.is_valid():
        userid = form.cleaned_data['userid']
        passwd1 = form.cleaned_data['passwd1']
        passwd2 = form.cleaned_data['passwd2']
        keynum = form.cleaned_data['keynum']
        cityname = form.cleaned_data['cityname']
        fname = form.cleaned_data['fname']
        sname = form.cleaned_data['sname']
        if passwd1 <> passwd2:
            return HttpResponse(get_res_info('1','passwd err'))
        if User.objects.all().filter(username = userid):
            return HttpResponse(get_res_info('2','user already exist'))
        try:
            vcode = Telcode.objects.get(tel = userid).vcode
        except Telcode.DoesNotExist:
            return HttpResponse(get_res_info('3','auth code err'))
        if vcode <> keynum:
            return HttpResponse(get_res_info('3','auth code err'))
        u = User.objects.create_user(userid,'',passwd1)
        u.first_name = fname
        u.last_name = sname
        u.save()
        ui = Userinfo(userid = userid,username = fname+' '+sname,usercity=cityname,tel = userid,role='buyer')
        ui.save()
        uimg = Userimage(userid=userid,imgtype='head',img='userimgs/defhead.png')
        uimg.save()
        hx = signup_hx(str(ui.id))
        if hx == 'ok':
            return HttpResponse(get_res_info())
        else:
            return HttpResponse(get_res_info('1','huanxin signup err'))
    else:
        err = ''
        for e in form.errors:
            err = err+e+'->'+form.errors[e]+'|||'
        return HttpResponse(err)

def signin(request):
    form = Signin(request.POST)
    if form.is_valid():
        userid = form.cleaned_data['userid']
        passwd = form.cleaned_data['passwd']
        try:
            User.objects.get(username=userid)
        except User.DoesNotExist:
            return HttpResponse(get_res_info('2','userid does not exist!'))
        user = authenticate(username=userid, password=passwd)
        if user is not None:
            if user.is_active:
                login(request, user)
                u = Userinfo.objects.get(userid=userid)
                res = {}
                res['rescode'] = '0'
                res['resmsg'] = 'ok'
                res['role'] = u.role
                
                ret = HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
                ret.set_cookie('id', userid,max_age=604800)
                ret.set_cookie('username', u.username,max_age=604800)
                head = Userimage.objects.get(userid=u.userid,imgtype='head').img.url
                ret.set_cookie('head', head,max_age=604800)
                return ret
            else:
                return HttpResponse(get_res_info('1','password incorrect!'))
        else:
            return HttpResponse(get_res_info('1','password incorrect!'))
    else:
        err = ''
        for e in form.errors:
            err = err+e+'->'+form.errors[e]+'|||'
        return HttpResponse(err)

def wxsignin(request):
    openid = request.POST.get('openid','')
    nickname = request.POST.get('nickname','')
    sex = request.POST.get('sex','')
    province = request.POST.get('province','')
    city = request.POST.get('city','')
    country = request.POST.get('country')
    headimgurl = request.POST.get('headimgurl','')
    privilege = request.POST.get('privilege','')
    unionid = request.POST.get('unionid','')
    try:
        wx = Wechat_info.objects.get(unionid=unionid)
    except Wechat_info.DoesNotExist:
        wx = Wechat_info()
        ui = Userinfo(userid=unionid,username=nickname,usercity=city,wechatid=unionid,role='buyer')
        ui.save()
        hx = signup_hx(str(ui.id))
        if hx <> 'ok':
            ui.delete()
            return HttpResponse(get_res_info('1','huanxin signup err'))
    wx.openid = openid
    wx.nickname = nickname
    wx.sex = sex
    wx.province = province
    wx.city = city
    wx.country = country
    wx.headimgurl = headimgurl
    wx.privilege = privilege
    wx.unionid = unionid
    wx.save()
    return HttpResponse(get_res_info())

def wx_binding(request):
    unionid = request.POST.get('unionid')
    tel = request.POST.get('tel')
    passwd1 = request.POST.get('passwd1')
    passwd2 = request.POST.get('passwd2')
    keynum = request.POST.get('keynum')
    if passwd1 <> passwd2:
        return HttpResponse(get_res_info('1','passwd err'))
    if User.objects.all().filter(username = tel):
        return HttpResponse(get_res_info('2','tel already used'))
    try:
        vcode = Telcode.objects.get(tel = tel).vcode
    except Telcode.DoesNotExist:
        return HttpResponse(get_res_info('3','auth code err'))
    if vcode <> keynum:
        return HttpResponse(get_res_info('3','auth code err'))
    u = User.objects.create_user(tel,'',passwd1)
    u.save()
    ui = Userinfo.objects.get(userid=unionid)
    ui.userid = tel
    ui.save()
    try:
        uimg = Userimage.objects.get(userid=unionid,imgtype='head')
    except:
        uimg = Userimage(userid=tel,imgtype='head',img='userimgs/defhead.png')
    uimg.userid = tel
    uimg.save()
    return HttpResponse(get_res_info())
    
def logout(request):
    logout(request)
    return HttpResponse(get_res_info())

def is_login(request):
    if request.user.is_authenticated():
        return HttpResponse(get_res_info('0','is login'))
    else:
        return HttpResponse(get_res_info('1','is not login'))

def send_mobile(request):
    tel = request.GET.get('tel')
    vcode = ''
    for i in range(6):
        vcode += str(random.randint(0, 9))
    try:
        tc = Telcode.objects.get(tel=tel)
        tc.vcode = vcode
    except Telcode.DoesNotExist:
        tc= Telcode(tel=tel,vcode=vcode)
    tc.save()
    res = send_mobile_vcode(tel, vcode)
    if '<message>ok</message>' in res:
        return HttpResponse(get_res_info())
    else:
        return HttpResponse(get_res_info('1',res))

def get_passwd(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        newpasswd = ''
        for i in range(8):
            newpasswd += str(random.randint(0, 9))
        try:
            u = User.objects.get(username=userid)
            u.set_password(newpasswd)
            u.save()
        except User.DoesNotExist:
            return HttpResponse(get_res_info('1','user does not exist'))
        email = Userinfo.objects.get(userid=userid).email
        send_mail_vcode(email, newpasswd)
        return HttpResponse(get_res_info())

def set_passwd(request):
    form = Setpasswd(request.POST)
    if form.is_valid():
        userid = form.cleaned_data['userid']
        passwd1 = form.cleaned_data['passwd1']
        passwd2 = form.cleaned_data['passwd2']
        passwd3 = form.cleaned_data['passwd3']
        user = authenticate(username=userid, password=passwd1)
        if user is not None:
            if user.is_active:
                if passwd2 == passwd3:
                    user.set_password(passwd2)
                    user.save()
                    return HttpResponse(get_res_info())
                else:
                    return HttpResponse(get_res_info('1','two password different!'))
            else:
                return HttpResponse(get_res_info('2','password incorrect!'))
        else:
            return HttpResponse(get_res_info('2','password incorrect!'))
    else:
        err = ''
        for e in form.errors:
            err = err+e+'->'+form.errors[e]+'|||'
        return HttpResponse(err)

def save_userinfo(request):
    userid = request.POST.get('userid')
    fname = request.POST.get('fname')
    sname = request.POST.get('sname')
    usercity = request.POST.get('usercity')
    tel = request.POST.get('tel')
    note = request.POST.get('note')
    email = request.POST.get('email')
    siteurl = request.POST.get('siteurl')
    assistant = request.POST.get('assistant')
    address = request.POST.get('address')
    selfintro = request.POST.get('selfintro')
    teamintro = request.POST.get('teamintro')
    corpintro = request.POST.get('corpintro')
    warning = request.POST.get('warning')
    agentid = request.POST.get('agentid')
    assistanttel = request.POST.get('assistanttel')
    creaid = request.POST.get('creaid')
    corp = request.POST.get('corp')
    creditcard = request.POST.get('creditcard')
    enddt = request.POST.get('enddt')
    cvs = request.POST.get('cvs')
    postid = request.POST.get('postid')
    try:
        u = Userinfo.objects.get(userid = userid)
    except Userinfo.DoesNotExist:
        u = Userinfo.objects.get(wechatid = userid)
    if fname <> None or sname <> None:
        u.username = fname+' '+sname
        try:
            user = User.objects.get(username = userid)
            user.first_name = fname
            user.last_name = sname
            user.save()
        except User.DoesNotExist:
            pass
    if usercity <> None:
        u.usercity = usercity
    if tel <> None:
        u.tel = tel
    if note <> None:
        cmd = note.strip()
        pattern = re.compile('charge\s+(.*?)\s+(.*)')
        items = re.findall(pattern, cmd)
        if len(items) == 0:
            u.note = note
        else:
            for item in items:
                sql1 = "select * from app.app_userinfo where role='agent' and userid='%s' " % item[1].strip()
                sql2 = "select * from app.t99_proxy_seller where userid='%s' and enabled='1' " % item[0].strip()
                if MySql.has_result(sql1) and MySql.has_result(sql2):
                    cp = Coupon(coupontype='d',userid=item[1].strip(),amt=9999999999,condi=item[0].strip()
                        ,startdt=datetime.datetime.strptime(get_now(),"%Y%m%d%H%M%S"),enddt=datetime.datetime.strptime(get_now(get_now(), 365)
                       ,"%Y%m%d%H%M%S"),usable='1',couponname='代理充值代金券')
                    cp.save()
                else:
                    pass
    if email <> None:
        u.email = email
    if siteurl <> None:
        cmd = siteurl.strip()
        pattern = re.compile('(\w+)charge(\d+)')
        items = re.findall(pattern, cmd)
        if len(items) == 0:
            u.siteurl = siteurl
        else:
            for item in items:
                if item[0] == 'add':
                    u.bal += int(item[1])
                elif item[0] == 'minus':
                    u.bal -= int(item[1])
    if assistant <> None:
        u.assistant = assistant
    if address <> None:
        u.address = address
    if selfintro <> None:
        u.selfintro = selfintro
    if teamintro <> None:
        u.teamintro = teamintro
    if corpintro <> None:
        u.corpintro = corpintro
    if warning <> None:
        u.warning = warning
    if agentid <> None:
        u.agentid = agentid
    if assistanttel <> None:
        u.assistanttel = assistanttel
    if creaid <> None:
        u.creaid = creaid
    if corp <> None:
        u.corp = corp
    if creditcard <> None:
        if u.creditcard == '':
            cp = Coupon(coupontype='c',userid=userid,amt=16.95
                        ,startdt=datetime.datetime.strptime(get_now(),"%Y%m%d%H%M%S"),enddt=datetime.datetime.strptime(get_now(get_now(), 7),"%Y%m%d%H%M%S"),usable='1',couponname='分享代金券')
            cp.save()
            send_auth(u.email)
        u.creditcard = creditcard
    if enddt <> None:
        u.enddt = enddt
    if cvs <> None:
        u.cvs = cvs
    if postid <> None:
        u.postid = postid
    u.save()
    return HttpResponse(get_res_info())

def save_temp(request):
    form = Temp(request.POST)
    if form.is_valid():
        userid = form.cleaned_data['userid']
        temptype = form.cleaned_data['temptype']
        temp = form.cleaned_data['temp']
        t = Template.objects.get(userid = userid,temptype = temptype)
        t.temp = temp
        t.save()
        return HttpResponse(get_res_info())
    else:
        err = ''
        for e in form.errors:
            err = err+e+'->'+form.errors[e]+'|||'
        return HttpResponse(err)

def get_temp(request):
    userid = request.GET.get('userid')
    temps = Template.objects.filter(userid = userid)
    res = []
    for t in temps:
        jsn = {}
        jsn['tempid'] = t.tempid
        jsn['temptype'] = t.temptype
        jsn['temp'] = t.temp
        res.append(jsn)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def free_edit(request):
    i = 0
    dataid = str(uuid.uuid1())
    userid = request.POST.get('userid')
    title = request.POST.get('title')
    pro = ''
    img_url = ''
    flag = True
    while request.POST.get('note'+str(i),'').strip() <> '' or request.FILES.get('img'+str(i),'') <> '':
        nt = request.POST.get('note'+str(i),'')
        img=request.FILES.get('img'+str(i),'')
        if flag and len(nt) > 0:
            pro = nt.decode('utf8')[:150].encode('utf8')
            flag = False
        f = Freeedit(dataid=dataid,userid=userid,note=nt,img=img,title=title)
        f.save()
        i = i + 1
    ss = Sharesite(htmlid = uuid.uuid1(),tempid = '',userid = userid,dataid = dataid,
                       sharetype = 'free',translated='0',shared='1')
    ss.save()
    url = 'http://' + request.META['HTTP_HOST'] + '/app/get/free/%s' % str(ss.id)
    ss.url = url
    ss.save()
    if userid not in ('info@webmainland.com',):
        uimgs = Userimage.objects.filter(userid=userid)
        for uimg in uimgs:
            if uimg.imgtype == 'ad':
                img_url = uimg.img.url
                break
            elif uimg.imgtype == 'head':
                img_url = uimg.img.url
        atc = Article(article_id=dataid,article_type='special_column',title=title,pro=pro,
                      img_url=img_url,article_url=url)
        atc.save()
    res = {}
    res['url'] = url
    res['htmlid'] = str(ss.htmlid)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def mk_html(request):
    form = Mkhtml(request.POST)
    if form.is_valid():
        tempid = form.cleaned_data['tempid']
        userid = form.cleaned_data['userid']
        dataid = form.cleaned_data['dataid']
        srtype = form.cleaned_data['srtype']
        tr = form.cleaned_data['tr']
        sr = form.cleaned_data['sr']
        labels = request.POST.get('labels','')
        try:
            if srtype == 'listing1':
                Listing.objects.get(listingid=dataid)
            elif srtype == 'listing2':
                Listing2.objects.get(listingid=dataid)
            elif srtype == 'article':
                Article.objects.get(article_id=dataid)
            elif srtype == 'mysite':
                Userinfo.objects.get(userid=dataid)
        except:
            return HttpResponse(get_res_info('2','dataid invalid'))
        if pay(userid,srtype,tr,False):
            temp = Template.objects.get(userid = userid,temptype=srtype).temp
            ss = Sharesite(htmlid = uuid.uuid1(),tempid = tempid,userid = userid,dataid = dataid,
                           sharetype = srtype,translated=tr,shared=sr,temp=temp,labels=labels)
            ss.save()
            url = 'http://' + request.META['HTTP_HOST'] + '/app/get/%s/%s' % (srtype,str(ss.id))
            ss.url = url
            ss.save()
            orderid = ''
            if tr == '1':
                order = Systemorder(htmlid=ss.htmlid,userid=userid,status='pending',dataid=dataid,
                                ordertype=srtype,transid='')
                order.save()
                orderid = order.id
                send_spread(userid,orderid)
            res = {}
            res['url'] = url
            res['rescode'] = '0'
            res['orderid'] = '' if tr == '0' else orderid
            res['htmlid'] = str(ss.htmlid)
            return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
        else:
            return HttpResponse(get_res_info('1','Insufficient account balance'))
    else:
        err = ''
        for e in form.errors:
            err = err+e+'->'+form.errors[e]+'|||'
        return HttpResponse(err)

def share_html(request):
    htmlid = request.POST.get('htmlid')
    try:
        s = Sharesite.objects.get(htmlid=htmlid)
        sd = Sharesite.objects.filter(userid=s.userid,dataid=s.dataid).count()
        print sd , s.translated
        if sd > 1 and s.translated <> '1':
            s.shared = '1'
            s.save()
            res = {}
            res['rescode'] = '0'
            res['resmsg'] = 'ok'
            res['url'] = s.url
            return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
            
        elif pay(s.userid,s.sharetype,s.translated,True):
            s.shared = '1'
            s.save()
            res = {}
            res['rescode'] = '0'
            res['resmsg'] = 'ok'
            res['url'] = s.url
            return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
        else:
            return HttpResponse(get_res_info('2','Insufficient account balance!'))
    except Sharesite.DoesNotExist:
        return HttpResponse(get_res_info('1','sharing html not exist!'))

def get_listing1_html(request,lid):
    s = Sharesite.objects.get(id = lid)
    s.visit = s.visit + 1
    s.save()
    l = Listing.objects.get(listingid = s.dataid)
    limgs = Listingimg.objects.filter(listingid = s.dataid,imgtype = 'listing1')
    maps = Listingimg.objects.filter(listingid = s.dataid,imgtype = 'map')
    try:
        vdo = Listingimg.objects.get(listingid = s.dataid,imgtype = 'mp4')
    except Listingimg.DoesNotExist:
        vdo = ''
    try:
        ad = Userimage.objects.get(userid = s.userid,imgtype = 'ad')
    except Userimage.DoesNotExist:
        ad = ''
    try:
        wechat = Userimage.objects.get(userid = s.userid,imgtype = 'wechat')
    except Userimage.DoesNotExist:
        wechat = ''
    uinfo = Userinfo.objects.get(userid = s.userid)
    comments = Sitecomment.objects.filter(htmlid=s.htmlid)
    temp = list(s.temp)
    tmp = {}
    for i in range(0,len(temp),2):
        tmp[temp[i]] = temp[i+1]
    title = get_title(l.listingid)
    his = Access_hitory(addr=request.META['REMOTE_ADDR'],actiontype='query',htmlid=s.htmlid
                    ,htmltype='listing1',userid=s.userid,agent=request.META['HTTP_USER_AGENT']
                        ,referer=request.META.get('HTTP_REFERER','url'))
    his.save()
    return render_to_response('listing1.html', {'l':l,'limgs':limgs,'ad':ad,'wechat':wechat,
                                       'uinfo':uinfo,'tmp':tmp,'s':s,'title':title,
                                       'comments':comments,'maps' : maps,'vdo':vdo})

def get_listing2_html(request,lid):
    s = Sharesite.objects.get(id = lid)
    s.visit = s.visit + 1
    s.save()
    l = Listing2.objects.get(listingid = s.dataid)
    limgs = Listingimg.objects.filter(listingid = s.dataid,imgtype = 'listing2')
    hux = Listingimg.objects.filter(listingid = s.dataid,imgtype = 'huxing')
    maps = Listingimg.objects.filter(listingid = s.dataid,imgtype = 'map')
    try:
        vdo = Listingimg.objects.get(listingid = s.dataid,imgtype = 'mp4')
    except Listingimg.DoesNotExist:
        vdo = ''
    try:
        ad = Userimage.objects.get(userid = s.userid,imgtype = 'ad')
    except Userimage.DoesNotExist:
        ad = ''
    try:
        wechat = Userimage.objects.get(userid = s.userid,imgtype = 'wechat')
    except Userimage.DoesNotExist:
        wechat = ''
    uinfo = Userinfo.objects.get(userid = s.userid)
    comments = Sitecomment.objects.filter(htmlid=s.htmlid)
    title = '%s|%s|%s' % (l.cityname,l.listingname,uinfo.username)
    temp = list(s.temp)
    tmp = {}
    for i in range(0,len(temp),2):
        tmp[temp[i]] = temp[i+1]
    his = Access_hitory(addr=request.META['REMOTE_ADDR'],actiontype='query',htmlid=s.htmlid
                    ,htmltype='listing2',userid=s.userid,agent=request.META['HTTP_USER_AGENT']
                        ,referer=request.META.get('HTTP_REFERER','url'))
    his.save()
    return render_to_response('listing2.html', {'l':l,'limgs':limgs,'ad':ad,'wechat':wechat,    
                                       'uinfo':uinfo,'tmp':tmp,'htmlid':s.htmlid,'comments':comments,
                                       'vdo':vdo,'hux':hux,'maps':maps,'title':title})

def get_mysite_html(request,lid):
    s = Sharesite.objects.get(id = lid)
    s.visit = s.visit + 1
    s.save()
    uinfo = Userinfo.objects.get(userid = s.dataid)
    team = Userimage.objects.filter(userid = s.dataid,imgtype = 'team')
    try:
        ad = Userimage.objects.get(userid = s.dataid,imgtype = 'ad')
    except Userimage.DoesNotExist:
        ad = ''
    try:
        wechat = Userimage.objects.get(userid = s.dataid,imgtype = 'wechat')
    except Userimage.DoesNotExist:
        wechat = ''
    history = Userimage.objects.filter(userid = s.dataid,imgtype = 'history')
    comm = Userimage.objects.filter(userid = s.dataid,imgtype = 'comment')
    try:
        vdo = Userimage.objects.get(userid = s.dataid,imgtype = 'mp4')
    except Userimage.DoesNotExist:
        vdo = ''
    title = '瑞安居|%s|%s' % (uinfo.usercity,uinfo.username)
    temp = list(s.temp)
    tmp = {}
    for i in range(0,len(temp),2):
        tmp[temp[i]] = temp[i+1]
    his = Access_hitory(addr=request.META['REMOTE_ADDR'],actiontype='query',htmlid=s.htmlid
                    ,htmltype='mysite',userid=s.userid,agent=request.META['HTTP_USER_AGENT']
                        ,referer=request.META.get('HTTP_REFERER','url'))
    his.save()
    return render_to_response('mysite.html', {'uinfo':uinfo,'ad':ad,'wechat':wechat,
                        'team':team,'history':history,'vdo':vdo,'comm':comm,'tmp':tmp,'title':title})

def get_article_html(request,lid):
    s = Sharesite.objects.get(id = lid)
    s.visit = s.visit + 1
    s.save()
    uinfo = Userinfo.objects.get(userid = s.userid)
    ad = ''
    wechat = ''
    vdo = ''
    try:
        ad = Userimage.objects.get(userid = s.userid,imgtype = 'ad')
        wechat = Userimage.objects.get(userid = s.userid,imgtype = 'wechat')
        vdo = Userimage.objects.get(userid = s.userid,imgtype = 'mp4')
    except Userimage.DoesNotExist:
        pass
    a = Article.objects.get(article_id = s.dataid)
    atype = get_code('t99_articletype', a.article_type)
    title = '%s|%s' % (atype,a.title)
    temp = list(s.temp)
    tmp = {}
    for i in range(0,len(temp),2):
        tmp[temp[i]] = temp[i+1]
    his = Access_hitory(addr=request.META['REMOTE_ADDR'],actiontype='query',htmlid=s.htmlid
                    ,htmltype='article',userid=s.userid,agent=request.META['HTTP_USER_AGENT']
                        ,referer=request.META.get('HTTP_REFERER','url'))
    his.save()
    return render_to_response('article.html', {'uinfo':uinfo,'ad':ad,'wechat':wechat,
                        'vdo':vdo,'s':s,'a':a,'tmp':tmp,'atype':atype,'title':title})

def get_free_edit_html(request,lid):
    s = Sharesite.objects.get(id = lid)
    s.visit = s.visit + 1
    s.save()
    frees = []
    dss = Freeedit.objects.filter(dataid = s.dataid)
    for ds in dss:
        jsn = {}
        jsn['note'] = ds.note
        jsn['title'] = ds.title
        jsn['img'] = 'none'
        if hasattr(ds.img,'url'):
            jsn['img'] = ds.img.url
        frees.append(jsn)
    ui = Userinfo.objects.get(userid=s.userid)
    editor = ui.username
    city = ui.usercity
    his = Access_hitory(addr=request.META['REMOTE_ADDR'],actiontype='query',htmlid=s.htmlid
                    ,htmltype='free',userid=s.userid,agent=request.META['HTTP_USER_AGENT']
                        ,referer=request.META.get('HTTP_REFERER','url'))
    his.save()
    title = '%s|%s|%s' % (dss[0].title,city,editor)
    response = render_to_response('freeedit.html', {'frees':frees,'s':s,'editor':editor,'title':title})
    return response

def download_app(request):
    if 'MicroMessenger' not in request.META['HTTP_USER_AGENT']:
        if 'iphone' in request.META['HTTP_USER_AGENT'].lower():
            his = Access_hitory(addr=request.META['REMOTE_ADDR'],actiontype='download',userid='apple',agent=request.META['HTTP_USER_AGENT']
                        ,referer=request.META.get('HTTP_REFERER','url'))
            his.save()
            return redirect('https://itunes.apple.com/cn/app/rui-an-ju/id1190756139?mt=8')
        new = Publish_apk.objects.all().order_by('-datadate')[0]
        res = redirect(new.apk.url)
        res['Content-Disposition'] = 'attachment; filename="*.apk"'
        his = Access_hitory(addr=request.META['REMOTE_ADDR'],actiontype='download',userid='android',agent=request.META['HTTP_USER_AGENT']
                        ,referer=request.META.get('HTTP_REFERER','url'))
        his.save()
        return res
    else:
        return render_to_response('wechattip.html')

def update_app(request):
    new = Publish_apk.objects.all().order_by('-datadate')[0]
    res = {}
    res['versioncode'] = new.versioncode
    res['versionname'] = new.versionName
    res['apkinfo'] = new.apkinfo
    res['apkurl'] = new.apk.url
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
    
def download_site(request):
    return render_to_response('download.html')

def submit_comment(request):
    form = Submitcomm(request.POST)
    if form.is_valid():
        htmlid = form.cleaned_data['htmlid']
        commtype = form.cleaned_data['commtype']
        userid = form.cleaned_data['userid']
        usercomm = form.cleaned_data['usercomm']
        if commtype in ('good','stars'):
            try:
                Sitecomment.objects.get(htmlid = htmlid,commtype=commtype,userid = userid)
                return HttpResponse(get_res_info('1','already followed!'))
            except Sitecomment.DoesNotExist:
                sc = Sitecomment(htmlid = htmlid,commtype=commtype,userid = userid,usercomment = usercomm)
                sc.save()
        else:
            sc = Sitecomment(htmlid = htmlid,commtype=commtype,userid = userid,usercomment = usercomm)
            sc.save()
        if commtype == 'comm':
            try:
                s = Sharesite.objects.get(htmlid=htmlid)
                s.comm = s.comm+1
                s.save()
            except Sharesite.DoesNotExist:
                pass
        elif commtype == 'good':
            try:
                s = Sharesite.objects.get(htmlid=htmlid)
                s.good = s.good+1
                s.save()
            except Sharesite.DoesNotExist:
                s = Listing.objects.get(listingid=htmlid)
                s.good = s.good+1
                s.save()
        elif commtype in ('order','stars'):
            o = Systemorder.objects.get(id=htmlid)
            o.status = 'commented'
            o.save()
        return HttpResponse(get_res_info())
    else:
        err = ''
        for e in form.errors:
            err = err+e+'->'+form.errors[e]+'|||'
        return HttpResponse(err)

def get_comments(request):
    htmlid = request.GET.get('htmlid')
    commtype = request.GET.get('commtype')
    coms = Sitecomment.objects.filter(htmlid=htmlid,commtype=commtype).order_by('commtime')
    res = []
    for com in coms:
        jsn = {}
        username = Userinfo.objects.get(userid=com.userid).username
        try:
            head = Userimage.objects.get(userid=com.userid,imgtype='head').img.url
        except Userimage.DoesNotExist:
            head = ''
        jsn['username'] = username
        jsn['head'] = head
        jsn['commtime'] = com.commtime.strftime('%Y-%m-%d')
        jsn['comment'] = com.usercomment
        res.append(jsn)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def save_listing2(request):
    listingid = request.POST.get('listingid')
    listingname = request.POST.get('listingname')
    cityname = request.POST.get('cityname')
    address = request.POST.get('address')
    proaddress = request.POST.get('proaddress')
    price1 = request.POST.get('price1','--')
    price1 = '--' if price1 == '' else price1
    price2 = request.POST.get('price2','--')
    price2 = '--' if price2 == '' else price2
    areas = request.POST.get('areas')
    postid = request.POST.get('postid')
    housetype = request.POST.get('housetype')
    intro = request.POST.get('intro')
    corp = request.POST.get('corp')
    warning = request.POST.get('warning')
    opendate = request.POST.get('opendate')
    try:
        l2 = Listing2.objects.get(listingid = listingid)
        l2.listingname = listingname
        l2.cityname = cityname
        l2.address = address
        l2.proaddress = proaddress
        l2.price1 = price1+'万元'
        l2.price2 = price2+'万元'
        l2.areas = areas
        l2.postid = postid
        l2.housetype = housetype
        l2.intro = intro
        l2.corp = corp
        l2.warning = warning
        l2.opendate = opendate
        l2.save()
        return HttpResponse(get_res_info())
    except Listing2.DoesNotExist:
        nl2 = Listing2(listingid = str(uuid.uuid1()),listingname = listingname,
                       cityname = cityname,address = address,proaddress = proaddress,
                       price1 = price1+'万元',price2 = price2+'万元',areas = areas,postid = postid,
                       housetype = housetype,intro = intro,corp = corp,warning = warning,
                       opendate = opendate)
        nl2.save()
        res = {}
        res['rescode'] = '0'
        res['resmsg'] = 'ok'
        res['listingid'] = nl2.listingid
        return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def get_listing2(request):
    searchof = request.GET.get('searchof')
    a = Listing2.objects.filter(listingname__icontains = searchof)
    b = Listing2.objects.filter(address__icontains = searchof)
    c = Listing2.objects.filter(postid__icontains = searchof)
    res = []
    for l2 in (a,b,c):
        for l in l2:
            jsn = {}
            jsn['listingid'] = l.listingid
            jsn['listingname'] = l.listingname
            jsn['cityname'] = l.cityname
            jsn['address'] = l.address
            jsn['proaddress'] = l.proaddress
            jsn['areas'] = l.areas
            jsn['postid'] = l.postid
            jsn['housetype'] = l.housetype
            jsn['intro'] = l.intro
            jsn['corp'] = l.corp
            jsn['warning'] = l.warning
            jsn['opendate'] = l.opendate
            jsn['price1'] = l.price1.replace('万元','')
            jsn['price2'] = l.price2.replace('万元','')
            jsn['imgurl'] = []
            jsn['huxing'] = []
            imgs = Listingimg.objects.filter(listingid = l.listingid)
            jsn['map'] = ''
            jsn['mp4'] = ''
            for img in imgs:
                if img.imgtype == 'listing2':
                    jsn['imgurl'].append(img.img.url)
                elif img.imgtype == 'map':
                    jsn['map'] = img.img.url
                elif img.imgtype == 'mp4':
                    jsn['mp4'] = img.img.url
                elif img.imgtype == 'huxing':
                    jsn['huxing'].append(img.img.url)
            res.append(jsn)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
    
def get_listing1(request):
    if request.method == 'GET':
        listingid = request.GET.get('listingid')
        try:
            l = Listing.objects.get(listingid__iexact = listingid)
        except Listing.DoesNotExist:
            return HttpResponse(get_res_info('1','no listing'))
        imgs = Listingimg.objects.filter(listingid__iexact = listingid)
        imgurl = []
        resjson = {}
        resjson['map'] = ''
        resjson['mp4'] = ''
        for img in imgs:
            if img.imgtype == 'listing1':
                imgurl.append(img.img.url)
            elif img.imgtype == 'map':
                resjson['map'] = img.img.url
            elif img.imgtype == 'mp4':
                resjson['mp4'] = img.img.url
        resjson['listingid'] = l.listingid
        resjson['listingname'] = l.listingname
        resjson['cityname'] = get_code('t99_cityname', l.cityname)
        resjson['price'] = l.price
        resjson['areas'] = l.areas
        resjson['bedroom'] = l.bedroom
        resjson['toilet'] = l.toilet
        resjson['parking'] = l.parking
        resjson['tax'] = l.tax
        resjson['housetype'] = l.housetype
        resjson['housestyle'] = l.housestyle
        resjson['basement'] = l.basement
        resjson['builddate'] = l.builddate
        resjson['intro'] = l.intro
        resjson['goodat'] = l.goodat
        resjson['corp'] = l.corp
        resjson['warning'] = l.warning
        resjson['url'] = l.url
        resjson['intro_eng'] = l.intro_eng
        resjson['imgurl'] = imgurl
        a = json.dumps(resjson,indent = 2,ensure_ascii=False)
        return HttpResponse(a)

def save_userimg(request):
    userid = request.POST.get('id')
    imgtype = request.POST.get('imgtype')
    imgurls = []
    if imgtype in ['ad','wechat','head','mp4',]:
        try:
            u = Userimage.objects.get(userid = userid,imgtype = imgtype)
        except Userimage.DoesNotExist:
            u = Userimage(userid = userid,imgtype = imgtype)
        if not request.FILES.get('img0'):
            return HttpResponse(get_res_info('1','img0 has no file'))
        u.img = request.FILES.get('img0')
        u.save()
        imgurls = u.img.url
    else:
        us = Userimage.objects.filter(userid = userid,imgtype = imgtype)
        for u in us:
            u.delete()
        for key in request.FILES.keys():
            if not request.FILES.get(key):
                return HttpResponse(get_res_info('1','%s has no file' % key))
            img = request.FILES.get(key)
            u2 = Userimage(userid = userid,imgtype = imgtype,img = img)
            u2.save()
            imgurls.append(u2.img.url)
    return HttpResponse(get_res_info('0',imgurls))

def save_listingimg(request):
    listingid = request.POST.get('id')
    imgtype = request.POST.get('imgtype')
    imgurls = []
    if imgtype in ['mp4','map',]:
        try:
            u = Listingimg.objects.get(listingid = listingid,imgtype = imgtype)
        except Listingimg.DoesNotExist:
            u = Listingimg(listingid = listingid,imgtype = imgtype,imgname=uuid.uuid1())
        if not request.FILES.get('img0'):
            return HttpResponse(get_res_info('1','img0 has no file'))
        u.img = request.FILES.get('img0')
        u.save()
        imgurls.append(u.img.url)
    else:
        us = Listingimg.objects.filter(listingid = listingid,imgtype = imgtype)
        for u in us:
            u.delete()
        for key in request.FILES.keys():
            if not request.FILES.get(key):
                return HttpResponse(get_res_info('1','%s has no file' % key))
            img = request.FILES.get(key)
            u2 = Listingimg(listingid = listingid,imgtype = imgtype,imgname = uuid.uuid1(),img = img)
            u2.save()
            imgurls.append(u2.img.url)
    return HttpResponse(get_res_info('0',imgurls))

def charge(request):
    form = Payinfo(request.POST)
    if form.is_valid():
        token = form.cleaned_data['token']
        amt = form.cleaned_data['amt']
        amty = int(amt)/100
        curr = form.cleaned_data['curr']
        userid = form.cleaned_data['userid']
        if curr <> 'CAD':
            return HttpResponse(get_res_info('1','please charge with CAD'))
        chargeres = charge_by_stripe(token, amt, curr)
        dis = Discount.objects.get(endamt=amty).percent
        tip = amty*float(dis)
        if chargeres <> 'ok':
            return HttpResponse(chargeres)
        u = Userinfo.objects.get(userid=userid)
        u.bal = float(u.bal)+amty+tip
        u.save()
        his = Charge_history(userid=userid,cardid=u.creditcard,cvs=u.cvs,enddt=u.enddt
                             ,curr=curr,amt=amty,tax=0.05,discount=tip,invoiced='0')
        his.save()
        return HttpResponse(get_res_info())
    else:
        err = ''
        for e in form.errors:
            err = err+e+'->'+form.errors[e]+'|||'
        return HttpResponse(err)

def get_recommendation(request):
    page = int(request.GET.get('page',1)) * 10
    rcmdtype = request.GET.get('rcmdtype')
    cityid = request.GET.get('cityid')
    objs = ''
    if rcmdtype == 'prischool':
        objs = School_dist.objects.filter(schoolcity=get_code2('t99_cityname', cityid)\
                ,schooltype__icontains='小学').order_by('-schoolid')[page-10:page]
    elif rcmdtype == 'midschool':
        objs = School_dist.objects.filter(schoolcity=get_code2('t99_cityname', cityid)\
                ,schooltype__icontains='中学').order_by('-schoolid')[page-10:page]
    elif rcmdtype == 'newhouse':
        objs = Listing.objects.filter(builddate=get_now()[:4],cityname=cityid).order_by('-datadate')[page-10:page]
    elif rcmdtype == 'bighouse':
        objs = Listing.objects.raw("SELECT * FROM app.app_listing WHERE CAST(bedroom AS SIGNED) >= 5\
                                     and cityname = '%s' order by datadate desc " % cityid)[page-10:page]
    elif rcmdtype == 'villa':
        objs = Listing.objects.raw("""SELECT a.* FROM app.app_listing a
        INNER JOIN (
        SELECT a.cityname,SUBSTRING_INDEX(GROUP_CONCAT(listingid ORDER BY datadate DESC),',',1) AS listingid
        FROM app.app_listing a
        INNER JOIN
        (SELECT cityname,
        SUBSTRING_INDEX(SUBSTRING_INDEX(GROUP_CONCAT(DISTINCT CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC),',',CEIL(COUNT(DISTINCT price)*0.05)),',',-1) AS p
        FROM app.app_listing GROUP BY cityname) b
        ON a.cityname = b.cityname
        WHERE CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) >= b.p
        GROUP BY cityname) b
        ON a.listingid = b.listingid
        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC""")[page-10:page]
    elif rcmdtype == 'land':
        objs = Listing.objects.raw("SELECT * FROM app.app_listing a\
        INNER JOIN (SELECT listingid FROM app.app_listingimg GROUP BY listingid) c\
        ON a.listingid = c.listingid\
        WHERE a.bedroom = '' AND toilet = '' and cityname = '%s' order by datadate desc " % cityid)[page-10:page]
    else:
        return HttpResponse(get_res_info('1','invalid rcmdtype'))
    res = []
    for obj in objs:
        jsn = make_rcmd_info(obj, 'school' if 'school' in rcmdtype else 'listing',request)
        res.append(jsn)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def get_school_listings(request):
    page = int(request.GET.get('page',1)) * 10
    schoolid = request.GET.get('schoolid')
    city = School_dist.objects.get(schoolid=schoolid).schoolcity
    listingcity = get_code3('t99_cityname', city)
    objs = Listing.objects.filter(cityname=listingcity).order_by('-datadate')[page-10:page]
    res = []
    for obj in objs:
        jsn = make_rcmd_info(obj, 'listing',request)
        res.append(jsn)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def get_cityinfo(request):
    sch = request.GET.get('school')
    res = []
    sql = 'select codename,descrition from app.t99_cityname order by orderid'
    if sch == '1':
        sql = 'select codename,descrition from app.t99_cityname where descrition2 is not null order by orderid '
    for row in MySql.sel_table(sql):
        city = {}
        city['cityid'] = row[0]
        city['cityname'] = row[1]
        res.append(city)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def get_article_type_info(request):
    res = []
    sql = "SELECT DISTINCT codename,descrition FROM app.t99_articletype  ORDER BY sortid ASC"
    for row in MySql.sel_table(sql):
        atc = {}
        atc['atypeid'] = row[0]
        atc['atypename'] = row[1]
        res.append(atc)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def get_shares(request):
    """stype说明: listings-发现页房源,mysites-发现页人个主页
                 articles-发现页文章,pending-待翻译,completed-待分享,shared-待评价
                 mylistings1-在售分享记录,mylistings2-预售分享记录,myarticles-文章分享记录"""
    page = int(request.GET.get('page',1)) * 10
    userid = request.GET.get('userid')
    stype = request.GET.get('stype')
    shrs = ''
    if stype == 'listing1':
        shrs = Sharesite.objects.filter(sharetype ='listing1',shared='1').filter(~Q(userid='wechat')&~Q(userid='info@webmainland.com'))\
                .order_by('-sharetime')[page-10:page]
    elif stype == 'listing2':
        shrs = Sharesite.objects.filter(sharetype ='listing2',shared='1').filter(~Q(userid='wechat')&~Q(userid='info@webmainland.com'))\
                .order_by('-sharetime')[page-10:page]
    elif stype == 'mysites':
        shrs = Sharesite.objects.filter(sharetype = 'mysite',shared='1').filter(~Q(userid='wechat')&~Q(userid='info@webmainland.com'))\
                .order_by('-sharetime')[page-10:page]
    elif stype == 'articles':
        shrs = Sharesite.objects.filter(sharetype = 'article',shared='1').filter(~Q(userid='wechat')&~Q(userid='info@webmainland.com'))\
                    .order_by('-sharetime')[page-10:page]
    elif stype == 'pending':
        orders = Systemorder.objects.filter(userid=userid,status='pending')
        a = [od.htmlid for od in orders]
        shrs = Sharesite.objects.filter(htmlid__in = a).order_by('-sharetime')[page-10:page]
    elif stype == 'completed':
        orders = Systemorder.objects.filter(userid=userid,status='completed')
        a = [od.htmlid for od in orders]
        shrs = Sharesite.objects.filter(htmlid__in = a).order_by('-sharetime')[page-10:page]
    elif stype == 'shared':
        shrs = Systemorder.objects.filter(userid=userid,status='shared').order_by('-starttime')[page-10:page]
    elif stype == 'commented':
        shrs = Systemorder.objects.filter(userid=userid,status='commented').order_by('-starttime')[page-10:page]
    elif stype == 'mylistings1':
        shrs = Sharesite.objects.filter(sharetype = 'listing1',userid = userid,shared='1')\
                .order_by('-sharetime')[page-10:page]
    elif stype == 'mylistings2':
        shrs = Sharesite.objects.filter(sharetype = 'listing2',userid = userid,shared='1')\
                .order_by('-sharetime')[page-10:page]
    elif stype == 'myarticles':
        shrs = Sharesite.objects.filter(sharetype = 'article',userid = userid,shared='1')\
                .order_by('-sharetime')[page-10:page]
    elif stype == 'mygood':
        coms = Sitecomment.objects.filter(userid=userid,commtype='good').order_by('-commtime')[page-10:page]
        a = [c.htmlid for c in coms]
        shrs = []
        for i in a:
            if len(i) < 20:
                try:
                    ll = Listing.objects.get(listingid=i)
                    shrs.append(ll)
                except Listing.DoesNotExist:
                    pass
            else:
                try:
                    ss = Sharesite.objects.get(htmlid = i)
                    shrs.append(ss)
                except Sharesite.DoesNotExist:
                    pass
    elif stype == 'search':
        searchof = request.GET.get('searchof')
        searchof = searchof.strip().lower()
        pattern = re.compile('[a-z]\d{7}')
        items = re.match(pattern, searchof)
        if items:
            shrs = Sharesite.objects.filter(dataid=searchof)[page-10:page]
        else:
            us = Userinfo.objects.filter(username__icontains=searchof)
            shrs = Sharesite.objects.filter(userid__in=[u.userid for u in us])[page-10:page]
    elif stype == 'filter':
        price1 = request.GET.get('price1')
        price2 = request.GET.get('price2')
        ltype = request.GET.get('ltype')
        bedroom = request.GET.get('bedroom')
        toilet = request.GET.get('toilet')
        lstyle = request.GET.get('lstyle')
        auth = request.GET.get('auth')
        listingids = filter_listing(price1,price2,ltype,bedroom,toilet,lstyle)
        if auth == '1':
            userids = authed_user()
            shrs = Sharesite.objects.filter(dataid__in=listingids,userid__in=userids)[page-10:page]
        else:
            shrs = Sharesite.objects.filter(dataid__in=listingids)[page-10:page]
    res = {}
    res['listing1'] = []
    res['listing2'] = []
    res['article'] = []
    res['mysite'] = []
    res['rcmdlisting'] = []
    if stype in ['shared','commented']:
        for od in shrs:
            ls = Sharesite.objects.get(htmlid=od.htmlid)
            jsn =  make_json(ls)
            jsn['orderid'] = str(od.id)
            jsn['orderdate'] = od.starttime.strftime('%Y-%m-%d')
            if stype == 'commented':
                stars = Sitecomment.objects.get(htmlid=od.id,commtype='stars').usercomment
                jsn['stars'] = stars
            res[jsn['sharetype']].append(jsn)
    elif stype == 'mygood':
        for ls in shrs:
            if isinstance(ls,Sharesite):
                jsn =  make_json(ls)
                res[jsn['sharetype']].append(jsn)
            else:
                jsn =  make_rcmd_info(ls,'listing',request)
                res['rcmdlisting'].append(jsn)
    else:
        for ls in shrs:
            jsn =  make_json(ls)
            res[jsn['sharetype']].append(jsn)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
        
def get_userinfo(request):
    userid = request.GET.get('userid')
    try:
        u = Userinfo.objects.get(userid = userid)
    except Userinfo.DoesNotExist:
        u = Userinfo.objects.get(wechatid = userid)
    first_name = ''
    last_name = ''
    try:
        user = User.objects.get(username = userid)
        first_name = user.first_name
        last_name = user.last_name
    except User.DoesNotExist:
        first_name = u.username.split(' ')[0]
        last_name = u.username.split(' ')[-1]
    uimg = Userimage.objects.filter(userid = userid)
    pending = Systemorder.objects.filter(userid = userid,status='pending').count()
    completed = Systemorder.objects.filter(userid = userid,status='completed').count()
    shared = Systemorder.objects.filter(userid = userid,status='shared').count()
    sr = Sharesite.objects.filter(userid=userid,shared='1',sharetype__in=['listing1','listing2','article'])
    sr1 = 0
    sr2 = 0
    sr3 = 0
    for s in sr:
        if s.sharetype == 'listing1':
            sr1 = sr1 + 1
        elif s.sharetype == 'listing2':
            sr2 = sr2 + 1
        elif s.sharetype == 'article':
            sr3 = sr3 + 1
    res = {}
    res['ad'] = ''
    res['wechat'] = ''
    res['head'] = ''
    res['mp4'] = ''
    team = []
    history = []
    comment = []
    for ui in uimg:
        if ui.imgtype == 'ad':
            res['ad'] = ui.img.url
        elif ui.imgtype == 'wechat':
            res['wechat'] = ui.img.url
        elif ui.imgtype == 'head':
            res['head'] = ui.img.url
        elif ui.imgtype == 'mp4':
            res['mp4'] = ui.img.url
        elif ui.imgtype == 'team':
            team.append(ui.img.url)
        elif ui.imgtype == 'history':
            history.append(ui.img.url)
        elif ui.imgtype == 'comment':
            comment.append(ui.img.url)
    res['team'] = team
    res['history'] = history
    res['comment'] = comment
    res['userid'] = u.userid
    res['fname'] = first_name
    res['sname'] = last_name
    res['usercity'] = u.usercity
    res['tel'] = u.tel
    res['note'] = u.note
    res['email'] = u.email
    res['siteurl'] = u.siteurl
    res['assistant'] = u.assistant
    res['address'] = u.address
    res['selfintro'] = u.selfintro
    res['teamintro'] = u.teamintro
    res['corpintro'] = u.corpintro
    res['warning'] = u.warning
    res['agentid'] = u.agentid
    res['assistanttel'] = u.assistanttel
    res['creaid'] = u.creaid
    res['corp'] = u.corp
    res['creditcard'] = u.creditcard
    res['cvs'] = u.cvs
    res['postid'] = u.postid
    res['enddt'] = u.enddt
    res['bal'] = float(u.bal)
    res['articlenum'] = str(int(float(u.bal)/0.99))
    res['listingnum'] = str(int(float(u.bal)/2.99))
    res['spreadnum'] = str(int(float(u.bal)/29.99))
    res['hxid'] = str(u.id)
    res['integrity'] = MySql.data_integrity(userid)
    res['pending'] = int(pending)
    res['completed'] = int(completed)
    res['shared'] = int(shared)
    res['sr1'] = int(sr1)
    res['sr2'] = int(sr2)
    res['sr3'] = int(sr3)
    res['priceurl'] = 'http://' + request.META['HTTP_HOST'] + '/static/img/price.png'
    res['mysite_visit'] = Access_hitory.objects.filter(userid=userid,htmltype='mysite')\
        .values('addr').distinct().count()
    res['mysite_share'] = Sharesite.objects.filter(userid=userid,sharetype='mysite').count()
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def get_articles(request):
    atype = request.GET.get('atype','')
    page = int(request.GET.get('page',1)) * 10
    atc = ''
    res = []
    if atype == '':
        atc = Article.objects.all().order_by('-datadate')[page-10:page]
    else:
        atc = Article.objects.filter(article_type = atype).order_by('-datadate')[page-10:page]
    for a in atc:
        jsn = {}
        jsn['article_id'] = a.article_id
        jsn['article_type_cn'] = get_code('t99_articletype', a.article_type)
        jsn['article_type'] = a.article_type
        jsn['title'] = a.title
        jsn['pro'] = a.pro
        jsn['img_url'] = a.img_url
        jsn['article_url'] = a.article_url
        jsn['eng_title'] = a.eng_title
        jsn['datatime'] = a.datadate.strftime('%Y-%m-%d')
        res.append(jsn)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def private_custom(request):
    cityname = request.POST.get('cityname')
    bedroom = request.POST.get('bedroom')
    toilet = request.POST.get('toilet')
    userid = request.POST.get('userid')
    username = request.POST.get('username')
    usercity = request.POST.get('usercity')
    tel = request.POST.get('tel')
    pricezone = request.POST.get('pricezone')
    buydate = request.POST.get('buydate')
    addservice = request.POST.get('addservice')
    housetype = request.POST.get('housetype')
    notes = request.POST.get('notes','')
    keynum = request.POST.get('keynum','')
    try:
        vcode = Telcode.objects.get(tel = tel).vcode
    except Telcode.DoesNotExist:
        return HttpResponse(get_res_info('3','auth code err'))
    if vcode <> keynum:
        return HttpResponse(get_res_info('3','auth code err'))
    c = Custom(cityname=cityname,bedroom=bedroom,toilet=toilet,userid=userid,
               username=username,usercity=usercity,tel=tel,pricezone=pricezone,
               buydate=buydate,addservice=addservice,housetype=housetype,notes=notes)
    c.save()
    send_private_custom(Userinfo.objects.get(userid=userid).email)
    send_custom(['yujh@realtoraccess.com','zhc@realtoraccess.com'],'您收到了一份私人订制定单，请查看')
    return HttpResponse(get_res_info())

def get_private_custom(request):
    userid = request.GET.get('userid')
    pcs = Custom.objects.filter(userid=userid)
    res = []
    for pc in pcs:
        jsn = {}
        jsn['cityname'] = pc.cityname
        jsn['bedroom'] = pc.bedroom
        jsn['toilet'] = pc.toilet
        jsn['userid'] = pc.userid
        jsn['username'] = pc.username
        jsn['usercity'] = pc.usercity
        jsn['tel'] = pc.tel
        jsn['pricezone'] = pc.pricezone
        jsn['buydate'] = pc.buydate
        jsn['addservice'] = pc.addservice
        jsn['datadate'] = pc.datadate.strftime('%Y-%m-%d')
        jsn['housetype'] = pc.housetype
        jsn['notes'] = pc.notes
        res.append(jsn)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def feedback(request):
    userid = request.POST.get('userid')
    problem = request.POST.get('problem')
    idea = request.POST.get('idea')
    tel = request.POST.get('tel')
    email = request.POST.get('email')
    img1 = request.FILES.get('img1','')
    img2 = request.FILES.get('img2','')
    img3 = request.FILES.get('img3','')
    f = Feedback(userid=userid,problem=problem,idea=idea,tel=tel,email=email,img1=img1,img2=img2,img3=img3)
    f.save()
    return HttpResponse(get_res_info())

def get_coupon(request):
    userid = request.GET.get('userid')
    cps = Coupon.objects.filter(userid=userid)
    res = {}
    res['available'] = []
    res['used'] = []
    res['expired'] = []
    for cp in cps:
        jsn = {}
        jsn['couponid'] = cp.couponid
        jsn['coupontype'] = cp.coupontype
        jsn['userid'] = cp.userid
        jsn['amt'] = float(cp.amt)
        jsn['startdt'] = cp.startdt.strftime('%Y-%m-%d')
        jsn['enddt'] = cp.enddt.strftime('%Y-%m-%d')
        jsn['usable'] = cp.usable
        jsn['couponname'] = cp.couponname
        if jsn['usable'] == '1' and jsn['amt'] > 0:
            res['available'].append(jsn)
        elif jsn['usable'] == '1' and jsn['amt'] == 0:
            res['used'].append(jsn)
        elif jsn['usable'] == '0':
            res['expired'].append(jsn)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
        
def get_ad(request):
    adtype = request.GET.get('adtype')
    ads = Advertisement.objects.filter(active='1',adtype=adtype)
    res = []
    for ad in ads:
        jsn = {}
        jsn['imgurl'] = ad.img.url
        jsn['adurl'] = ad.url
        res.append(jsn)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def get_charge_history(request):
    userid = request.GET.get('userid')
    chs = Charge_history.objects.filter(userid=userid)
    res = {}
    res['invoiceyes'] = []
    res['invoiceno'] = []
    for ch in chs:
        jsn = {}
        jsn['chargeid'] = ch.id
        jsn['userid'] = ch.userid
        jsn['cardid'] = ch.cardid
        jsn['cvs'] = ch.cvs
        jsn['enddt'] = ch.enddt
        jsn['curr'] = ch.curr
        jsn['amt'] = float(ch.amt)
        jsn['tax'] = float(ch.tax)
        jsn['discount'] = float(ch.discount)
        jsn['invoiced'] = ch.invoiced
        jsn['datadate'] = ch.datadate.strftime('%Y-%m-%d %H:%M:%S')
        if jsn['invoiced'] == '0':
            res['invoiceno'].append(jsn)
        else:
            res['invoiceyes'].append(jsn)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def get_invoice(request):
    userid = request.POST.get('userid')
    chargeids = request.POST.get('chargeids')
    email = request.POST.get('email')
    addr = request.POST.get('addr')
    postid = request.POST.get('postid')
    for chargeid in chargeids.split(','):
        try:
            ci = Charge_history.objects.get(id=str(chargeid).strip(),userid=userid)
            if ci.invoiced == '0':
                ci.invoiced = '1'
                ci.save()
            else:
                return HttpResponse(get_res_info('2','chargeid %s invoiced' % chargeid))
        except Charge_history.DoesNotExist:
            return HttpResponse(get_res_info('1','chargeid %s not found' % chargeid))
    ih = Invoiced_history(chargeids=chargeids,userid=userid,email=email,addr=addr,postid=postid)
    ih.save()
    send_invoice(email)
    return HttpResponse(get_res_info())

def get_sys_msg(request):
    msgs = System_msg.objects.all().order_by('-datadate')
    res = []
    for msg in msgs:
        jsn = {}
        jsn['userid'] = msg.userid
        jsn['msgtype'] = msg.msgtype
        jsn['msgtitle'] = msg.msgtitle
        jsn['msg'] = msg.msg
        jsn['datadate'] = msg.datadate
        res.append(jsn)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def get_userinfo_hx(request):
    hxid = request.GET.get('hxid')
    ui = Userinfo.objects.get(id=int(hxid))
    head = Userimage.objects.get(userid=ui.userid,imgtype='head')
    res = {}
    res['username'] = ui.username
    res['head'] = head.img.url
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def get_static(request):
    res = []
    imgs = []
    imgs.append('http://' + request.META['HTTP_HOST'] + '/static/img/school.png')
    imgs.append('http://' + request.META['HTTP_HOST'] + '/static/img/newhouse.png')
    imgs.append('http://' + request.META['HTTP_HOST'] + '/static/img/bighouse.png')
    imgs.append('http://' + request.META['HTTP_HOST'] + '/static/img/villa.png')
    imgs.append('http://' + request.META['HTTP_HOST'] + '/static/img/land.png')
    names = []
    names.append('学区房源')
    names.append('1年新房源')
    names.append('5室以上房源')
    names.append('顶级豪宅')
    names.append('土地置购')
    types = []
    types.append('school')
    types.append('newhouse')
    types.append('bighouse')
    types.append('villa')
    types.append('land')
    for i in range(5):
        jsn = {}
        jsn['img'] = imgs[i]
        jsn['name'] = names[i]
        jsn['type'] = types[i]
        res.append(jsn)
    
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
    
def index(request):
    return render_to_response('xjq/Tea.html')
    
def xjq(request):
    return render_to_response('xjq/Tea.html')

def xjq_login(request):
    return render_to_response('xjq/signin.html')
    
def xjq_signup(request):
    return render_to_response('xjq/signup.html')

def test(request):
    return render_to_response('wechattip.html')
#     aa = Userimage.objects.all()
#     used = []
#     for a in aa:
#         used.append(a.img.path.split('/')[-1])
#     imgs = os.listdir('/root/myweb/data/userimgs')
#     for a in imgs:
#         if a not in used:
#             os.system('rm -f /root/myweb/data/userimgs/%s' % a)
#             print 'delete:',a
#     return HttpResponse('ok')
