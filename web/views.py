# -*- coding:utf-8 -*-
from app.models import *
from django.http import JsonResponse
from news.models import *
from web.models import *
from portal.models import MessageCenter
from singlepage.models import *
from django.shortcuts import HttpResponse, render_to_response, redirect
from django.db.models.fields.files import FieldFile
from myweb.itools import *
from math import *
import random
from itertools import chain
import json
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
import random
from mail_template import *
from excel import *
import os
from PIL import Image
import requests

dicts = []
for row in MySql.sel_table("select * from app.t99_cityname"):
    dicts.append(row)


def mail_api(email_type, recv_email, send_email, message_name, message_detial,
             message_phone='', password=123456):
    url = 'http://123.56.190.119:8055/api/values/send_email'
    params = {
        'type': email_type,
        'email': recv_email,
        'message_email': send_email,
        'message_name': message_name,
        'message_detial': message_detial,
        'message_phone': message_phone,
        'password': password,
    }

    res = requests.get(url, params=params)
    print params
    print res.status_code, res.json()


def get_res_info(code='0', msg='success'):
    res = {}
    res['rescode'] = code
    res['resdesc'] = msg
    return json.dumps(res, indent=2, ensure_ascii=False)


def success(data=None):
    if data is None:
        data = []
    res = dict()
    res['code'] = '00'
    res['message'] = '请求成功!'
    res['data'] = data

    return JsonResponse(res, encoder=MyEncoder)


def error(code='01', msg='', data=None):
    if data is None:
        data = {}
    res = dict()
    res['code'] = code
    res['message'] = msg
    res['data'] = data
    return JsonResponse(res, encoder=MyEncoder)


def get_distance(Lat_A, Lng_A, Lat_B, Lng_B):
    ra = 6378.140  # 赤道半径
    rb = 6356.755  # 极半径 （km）
    flatten = (ra - rb) / ra  # 地球偏率
    rad_lat_A = radians(Lat_A)
    rad_lng_A = radians(Lng_A)
    rad_lat_B = radians(Lat_B)
    rad_lng_B = radians(Lng_B)
    pA = atan(rb / ra * tan(rad_lat_A))
    pB = atan(rb / ra * tan(rad_lat_B))
    xx = acos(
        sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
    if xx == 0:
        return 0
    c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
    c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (xx + dr)
    return distance


def index(request):
    cnt = {}
    cnt['listing1'] = Listing.objects.all().count()
    cnt['listing2'] = Listing2.objects.all().count()
    cnt['today'] = 0
    for i in MySql.sel_table("""select count(*) from app.app_listing 
        where DATE_FORMAT(datadate,'%%Y%%m%%d') between %s and %s """ % (
            get_now(get_now(), -7, 'd')[:8], get_now()[:8])):
        cnt['today'] = i[0]
    cnt['agent'] = agent_info.objects.filter(active='1').count()
    cnt['school'] = School_dist.objects.all().count()

    article = {}
    atcs = Article_info.objects.raw("""SELECT * FROM news_article_info a
                    INNER JOIN (
                    SELECT  articletype,MAX(publishdate) AS dt FROM news_article_info
                    WHERE src = 'mp'
                    GROUP BY articletype
                    ) b
                    ON a.publishdate = b.dt
                    AND a.articletype = b.articletype""")
    for atc in atcs:
        article[atc.articletype] = {}
        article[atc.articletype]['articleid'] = atc.id
        article[atc.articletype]['title'] = atc.title

    #     agent = []
    #     rcmds = Systemorder.objects.filter(ordertype='mysite').order_by('-starttime')
    #     agents = [r.userid for r in rcmds]
    #     for a in agents:
    #         u = Userinfo.objects.get(userid=a,role='agent')
    #         tmp = {}
    #         img = Userimage.objects.get(userid=u.userid,imgtype='head')
    #         tmp['userid'] = u.userid
    #         tmp['username'] = u.username
    #         tmp['img'] = img.img.url
    #         agent.append(tmp)

    od = Systemorder.objects.filter(status='completed',
                                    ordertype__in=['listing1', 'sale',
                                                   'listing2', 'rent',
                                                   'mysite']).order_by(
        '-starttime')
    saling = []
    renting = []
    mysites = []

    for agent in agent_info.objects.raw("""
                    SELECT a.* 
                    FROM app.`web_agent_info` a
                    LEFT JOIN
                    (
                    SELECT userid,SUM(CASE WHEN service = 'auth' THEN 9
                                                WHEN service = 'vip' THEN 8
                                                ELSE 0 END) AS v
                    FROM app.`web_agent_auth` GROUP BY userid
                    ) b
                    ON a.`userid` = b.userid
                    where a.active = '1'
                    ORDER BY CASE WHEN b.v IS NULL THEN 0 ELSE b.v END DESC,
                    a.`datadate` DESC,
                    CASE WHEN a.username <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.tel <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.note <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.website <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.address <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.selfintro <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.corp <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.head <> 'agentimgs/def_head.png' THEN 1 ELSE -99 END+
                    CASE WHEN a.qrcode <> 'agentimgs/def_qrcode.png' THEN 1 ELSE 0 END+
                    CASE WHEN a.username2 <> '' THEN 1 ELSE 0 END DESC limit 20"""):
        jsn = {}
        jsn['uid'] = agent.id
        jsn['userid'] = agent.userid
        jsn['username'] = agent.username
        jsn['usercity'] = get_cityname(agent.city)
        jsn['corp'] = agent.corp
        jsn['note'] = agent.note
        jsn['auth'] = 1 if agent_auth.objects.filter(userid=agent.userid,
                                                     service='auth',
                                                     status='paid') else 0
        jsn['img'] = agent.head.url
        jsn['wechat'] = agent.qrcode.url
        mysites.append(jsn)

    for o in od:
        # 用户信息
        if o.ordertype in ['listing1', 'listing2']:
            s = Sharesite.objects.get(htmlid=o.htmlid)
            listingid = s.dataid
            sharetype = s.sharetype

            try:
                ui = agent_info.objects.get(userid=s.userid)
            except agent_info.DoesNotExist:
                continue
            uid = ui.id
            username = ui.username
            usercity = ui.city if ui.city != '' else '加拿大'
            corp = ui.corp
            head = ui.head.url
        elif o.ordertype in ['sale', 'rent']:
            s = Listing_for_sp.objects.get(id=o.htmlid)
            listingid = s.listingid
            sharetype = o.ordertype
            token = Tokens.objects.get(token=s.token)
            ui = agent_info.objects.get(userid=token.userid)
            uid = ui.id
            username = ui.username
            usercity = '加拿大'
            corp = 'Webmainland Single Website'
            head = ui.head.url
        jsn = {}
        jsn['lastpage'] = 99
        jsn['uid'] = uid
        jsn['head'] = head
        jsn['from'] = usercity + '经纪'
        jsn['username'] = username
        jsn['corp'] = corp

        limg = Listingimg.objects.filter(listingid=listingid,
                                         imgtype__in=['listing1', 'listing2'])
        jsn['img'] = ''
        for i in limg:
            jsn['img'] = i.img.url
            break

        if sharetype == 'listing1':
            li = Listing.objects.get(listingid=listingid)
            jsn['mls'] = li.listingid
            jsn['listingtype'] = 'listing1'
            jsn['addr'] = li.listingname
            jsn['price'] = li.price
            jsn['areas'] = li.areas
            jsn['cityname'] = li.cityname
            jsn['housetype'] = li.housetype
            jsn['visit'] = s.visit
            jsn['good'] = s.good
            jsn['date'] = s.sharetime.strftime('%Y-%m-%d')
            jsn['htmlid'] = '/web/listing1/' + li.listingid + '/' + s.htmlid
            saling.append(jsn)
        elif sharetype == 'listing2':
            li = Listing2.objects.get(listingid=listingid)
            jsn['mls'] = li.listingid
            jsn['listingname'] = li.listingname
            jsn['listingtype'] = 'listing2'
            jsn['addr'] = li.address
            jsn['price'] = li.price1
            jsn['areas'] = li.areas if li.areas.strip() <> '' else '-- sqft.'
            jsn['cityname'] = li.cityname
            jsn['housetype'] = li.housetype
            jsn['visit'] = s.visit
            jsn['good'] = s.good
            jsn['date'] = s.sharetime.strftime('%Y-%m-%d')
            jsn[
                'htmlid'] = '/web/listing2/?mls=' + li.listingid + '&htmlid=' + s.htmlid
            renting.append(jsn)
        elif sharetype == 'sale':
            jsn['mls'] = s.listingid
            jsn['listingname'] = s.listingname
            jsn['listingtype'] = 'sale'
            jsn['addr'] = s.listingname
            jsn['price'] = s.price
            jsn['corp'] = s.listingtype
            jsn['areas'] = s.areas if s.areas.strip() <> '' else '-- sqft.'
            jsn['cityname'] = s.cityname
            jsn['housetype'] = s.housetype
            jsn['visit'] = s.visit
            jsn['good'] = s.good
            jsn['date'] = s.datadate.strftime('%Y-%m-%d')
            jsn['htmlid'] = s.url
            saling.append(jsn)
        elif sharetype == 'rent':
            jsn['mls'] = s.listingid
            jsn['listingname'] = s.listingname
            jsn['listingtype'] = 'rent'
            jsn['addr'] = s.listingname
            jsn['price'] = s.price
            jsn['areas'] = s.areas if s.areas.strip() <> '' else '-- sqft.'
            jsn['cityname'] = s.cityname
            jsn['housetype'] = s.housetype
            jsn['visit'] = s.visit
            jsn['good'] = s.good
            jsn['date'] = s.datadate.strftime('%Y-%m-%d')
            jsn['htmlid'] = s.url
            renting.append(jsn)

    his = Access_hitory(addr=request.META.get('REMOTE_ADDR', ''),
                        actiontype='query', htmltype='index',
                        agent=request.META.get('HTTP_USER_AGENT', '')
                        , referer=request.META.get('HTTP_REFERER', 'url'))
    his.save()
    return render_to_response('web/index.html',
                              {'cnt': cnt, 'article': article, 'saling': saling,
                               'renting': renting,
                               'mysites': mysites})


def downloadapp(request):
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='appinstro',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'))
    his.save()
    return render_to_response('web/APP.html')


def sync_user(request):
    body = json.loads(request.body)
    userid = body.get('userid')
    passwd = body.get('passwd')
    fname = body.get('fname', '')
    lname = body.get('lname', '')
    token = body.get('token', '')
    stripeChargeId = body.get('stripeChargeId', '')

    MySql.run_sql(
        "insert into app.web_signup_channel values('%s','%s',now())" % (
            userid, 'sync from bright'))

    if token != '1D388DF8CA777DCBF1BCE3F7AAC07AEB174E9C4D':
        return error('03', '验证失败！')

    if User.objects.all().filter(username=userid):
        return error('02', '用户%s已存在' % userid)

    print(body)
    u = User.objects.create_user(userid, userid, passwd)
    u.save()
    agt = agent_info(userid=userid, email=userid, logo='agentimgs/def_logo.png',
                     head='agentimgs/def_head.png',
                     head2='agentimgs/def_head.png',
                     username='%s %s' % (fname, lname),
                     fname=fname,
                     lname=lname,
                     qrcode='agentimgs/def_qrcode.png',
                     qrcode2='agentimgs/def_qrcode.png')
    agt.save()


    agent_auth.objects.create(userid=userid,
                              service='engagement',
                              cardno=stripeChargeId,
                              status='paid')
    
    return success()


def listing_list(request):
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='houselist',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'))
    his.save()
    return render_to_response('web/houselist.html')


def get_nearby(srcdata):
    mycountyid = ''
    mycityid = ''
    mygroupid = ''

    nearby_county = []
    nearby_city = []
    for d in dicts:
        if d[10].lower() == srcdata.lower():
            mycountyid = d[0]
            mycityid = d[2]
            mygroupid = d[4]
            break

    for d in dicts:
        if d[2] == mycityid and d[0] != mycountyid:
            nearby_county.append([d[0], d[1]])
    for d in dicts:
        if d[4] == mygroupid and d[2] != mycityid:
            nearby_city.append([d[2], d[3]])

    if len(nearby_county) == 0:
        return {'nearlev': 'city', 'nearby': nearby_city}
    else:
        return {'nearlev': 'county', 'nearby': nearby_county}


def listingpage_redirect(request):
    mls = request.GET.get('mls')
    htmlid = request.GET.get('htmlid', '')
    return redirect('/web/listing1/%s/%s' % (mls, htmlid), permanent=True)


def listingpage(request, mls, htmlid):
    listingid = mls
    if htmlid:
        try:
            ss = Sharesite.objects.get(htmlid=htmlid)
            ss.visit += 1
            ss.save()
        except Listing.DoesNotExist:
            return HttpResponse('no sharesite')
    try:
        listing = Listing.objects.get(listingid=listingid)
        listing.visit += 1
        listing.save()
        beds = listing.bedroom if listing.bedroom <> '' else '0'
        tol = listing.toilet[:1] if listing.toilet <> '' else '0'
        bedtol = '%s室%s卫' % (beds, tol)
        chartpara = {}
        chartpara['cityname'] = get_code('t99_cityname', listing.cityname)
        chartpara['housetype'] = listing.housetype
        chartpara['housetype_cn'] = get_housetype_name(listing.housetype)
    except Listing.DoesNotExist:
        return HttpResponse('no listing')
    limgs = Listingimg.objects.filter(listingid=listingid, imgtype='listing1')
    imgs = []
    for img in limgs:
        imgs.append(img.img.url)

    # 加工地址
    sql = "select countryname,provname,groupname,cityname,countyname,countryid,provid,groupid,cityid,countyid from app.t99_cityname where srcdata='%s' " % listing.cityname
    dict = {}
    for row in MySql.sel_table(sql):
        dict['country'] = row[0]
        dict['prov'] = row[1]
        dict['group'] = row[2]
        dict['city'] = row[3]
        dict['county'] = row[4]
        dict['countryid'] = row[5]
        dict['provid'] = row[6]
        dict['groupid'] = row[7]
        dict['cityid'] = row[8]
        dict['countyid'] = row[9]
    ss = Sharesite.objects.filter(sharetype='listing1',
                                  dataid=listingid).order_by('-sharetime')

    firstagent = 'diao.xc@gmail.com'
    if listingid == 'r2287114':
        firstagent = 'mwtsang@aol.com'
    elif listingid == 'r2301799':
        firstagent = 'yaletownrealtor@gmail.com'
    ui = agent_info.objects.get(userid=firstagent)
    agent = {}
    agent['id'] = ui.id
    agent['note'] = ui.note
    agent['usercity'] = ui.city if ui.city != '' else '加拿大'
    agent['username'] = ui.username
    agent['usertel'] = ui.tel
    agent['userid'] = ui.userid
    agent['corp'] = ui.corp
    agent['head'] = ui.head.url

    article = {}
    article['rcmd'] = []
    atcs = Article_info.objects.raw("""SELECT * FROM news_article_info a
                    INNER JOIN (
                    SELECT  articletype,MAX(publishdate) AS dt FROM news_article_info
                    WHERE src = 'mp'
                    GROUP BY articletype
                    ) b
                    ON a.publishdate = b.dt
                    AND a.articletype = b.articletype
                    order by a.publishdate desc""")
    for atc in atcs:
        tmp = {}
        tmp['title'] = atc.title
        tmp['articleid'] = atc.id
        tmp['date'] = atc.publishdate[:10]
        article['rcmd'].append(tmp)
        article[atc.articletype] = {}
        article[atc.articletype]['articleid'] = atc.id
        article[atc.articletype]['title'] = atc.title

    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='house1',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        htmlid=listingid)
    his.save()
    return render_to_response('web/house.html',
                              {'listing': listing,
                               'zh': translate_en2zh(listing.intro),
                               'chartpara': chartpara
                                  , 'bedtol': bedtol, 'imgs': imgs,
                               'agent': agent, 'article': article,
                               'listingtype': 'listing1', 'dict': dict,
                               'nearby': get_nearby(listing.cityname)})


def listingpage2(request):
    listingid = request.GET.get('mls')
    htmlid = request.GET.get('htmlid')
    if htmlid:
        try:
            ss = Sharesite.objects.get(htmlid=htmlid)
            ss.visit += 1
            ss.save()
        except Listing.DoesNotExist:
            return HttpResponse('no sharesite')
    try:
        listing2 = Listing2.objects.get(listingid=listingid)
        listing2.visit += 1
        listing2.save()
    except Listing2.DoesNotExist:
        return HttpResponse('no listing')
    listing = {}
    listing['listingid'] = '--'  # listing2.listingid
    listing['price'] = listing2.price1
    listing['areas'] = listing2.areas
    listing['parking'] = '--'
    listing['bedroom'] = '--'
    listing['toilet'] = '--'
    listing['tax'] = '--'
    listing['housetype'] = '预售楼盘'
    listing['housestyle'] = '--'
    listing['basement'] = '--'
    listing['builddate'] = listing2.opendate
    listing['corp'] = listing2.corp
    listing['goodat'] = ''
    listing['intro'] = listing2.intro
    limgs = Listingimg.objects.filter(listingid=listingid, imgtype='listing2')
    imgs = []
    for img in limgs:
        imgs.append(img.img.url)

    ss = Sharesite.objects.filter(sharetype='listing2',
                                  dataid=listingid).order_by('-sharetime')
    agents = []
    for ui in agent_info.objects.all().order_by('datadate'):
        jsn = {}
        jsn['note'] = ui.note
        jsn['usercity'] = ui.city if ui.city != '' else '加拿大'
        jsn['username'] = ui.username
        jsn['usertel'] = ui.tel
        jsn['userid'] = ui.userid
        jsn['corp'] = ui.corp
        jsn['head'] = ui.head.url
        agents.append(jsn)
        if len(agents) == 2:
            break

    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='house2',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        htmlid=listingid)
    his.save()
    return render_to_response('web/house.html',
                              {'listing': listing, 'imgs': imgs,
                               'agents': agents, 'listingtype': 'listing2'})


def get_rcmd_listing(request):
    ls = Listing.objects.all().order_by('-datadate')[:20]
    res = []
    for l in ls:
        li = Listingimg.objects.filter(listingid=l.listingid,
                                       imgtype='listing1')
        if not li:
            continue
        jsn = {}
        jsn['img'] = li[0].img.url
        jsn['city'] = l.cityname
        jsn['mls'] = l.listingid
        jsn['price'] = l.price
        jsn['housetype'] = l.housetype
        jsn['addr'] = l.listingname
        jsn['areas'] = l.areas
        jsn['visit'] = l.visit
        jsn['date'] = l.datadate.strftime('%Y-%m-%d')
        res.append(jsn)
        if len(res) == 4:
            break
    r = HttpResponse(json.dumps(res, indent=2, ensure_ascii=False))
    r["Access-Control-Allow-Origin"] = "*"
    return r


# def get_listing_spread(request):
#     page = int(request.GET.get('page','1')) * 4
#     ltype = request.GET.get('type','listing1')
#     if ltype == 'listing1':
#         od = Systemorder.objects.filter(status='completed',ordertype__in=['listing1','sale']).order_by('-starttime')
#     elif ltype == 'listing2':
#         od = Systemorder.objects.filter(status='completed',ordertype__in=['listing2','rent']).order_by('-starttime')
#     lastpage = int(ceil(len(od)/4.0))
#     res = []
#     for o in od[page-4:page]:
#         
#         #用户信息
#         if o.ordertype in ['listing1','listing2']:
#             s = Sharesite.objects.get(htmlid=o.htmlid)
#             listingid = s.dataid
#             sharetype = s.sharetype
#             
#             ui = Userinfo.objects.get(userid=s.userid)
#             username = ui.username
#             usercity = ui.usercity
#             corp = ui.corp
#             head = Userimage.objects.get(userid=s.userid,imgtype='head').img.url
#         else:
#             s = Listing_for_sp.objects.get(id=o.htmlid)
#             listingid = s.listingid
#             sharetype = o.ordertype
#             token = Tokens.objects.get(token=s.token)
#             ui = User_information.objects.get(email=token.userid)
#             username = ui.username
#             usercity = '加拿大'
#             corp = 'Webmainland Single Website'
#             head = ui.head.url
#         jsn = {}
#         jsn['lastpage'] = lastpage
#         jsn['head'] = head
#         jsn['from'] = usercity+'经纪'
#         jsn['username'] = username
#         jsn['corp'] = corp
#         
#         limg = Listingimg.objects.filter(listingid=listingid,imgtype__in=['listing1','listing2'])
#         jsn['img'] = ''
#         for i in limg:
#             jsn['img'] = i.img.url
#             break
#         if sharetype == 'listing1' and ltype == 'listing1':
#             li = Listing.objects.get(listingid=listingid)
#             jsn['mls'] = li.listingid
#             jsn['listingtype'] = 'listing1'
#             jsn['addr'] = li.listingname
#             jsn['price'] = li.price
#             jsn['areas'] = li.areas
#             jsn['cityname'] = li.cityname
#             jsn['housetype'] = li.housetype
#             jsn['visit'] = s.visit
#             jsn['good'] = s.good
#             jsn['date'] = s.sharetime.strftime('%Y-%m-%d')
#             jsn['htmlid'] = s.htmlid
#             res.append(jsn)
#         elif sharetype == 'listing2' and ltype == 'listing2':
#             li = Listing2.objects.get(listingid=listingid)
#             jsn['mls'] = li.listingid
#             jsn['listingname'] = li.listingname
#             jsn['listingtype'] = 'listing2'
#             jsn['addr'] = li.address
#             jsn['price'] = li.price1
#             jsn['areas'] = li.areas if li.areas.strip() <> '' else '-- sqft.'
#             jsn['cityname'] = li.cityname
#             jsn['housetype'] = li.housetype
#             jsn['visit'] = s.visit
#             jsn['good'] = s.good
#             jsn['date'] = s.sharetime.strftime('%Y-%m-%d')
#             jsn['htmlid'] = s.htmlid
#             res.append(jsn)
#         elif sharetype == 'sale' and ltype == 'listing1':
#             jsn['mls'] = s.listingid
#             jsn['listingname'] = s.listingname
#             jsn['listingtype'] = 'sale'
#             jsn['addr'] = s.listingname
#             jsn['price'] = s.price
#             jsn['corp'] = s.listingtype
#             jsn['areas'] = s.areas if s.areas.strip() <> '' else '-- sqft.'
#             jsn['cityname'] = s.cityname
#             jsn['housetype'] = s.housetype
#             jsn['visit'] = s.visit
#             jsn['good'] = s.good
#             jsn['date'] = s.datadate.strftime('%Y-%m-%d')
#             jsn['htmlid'] = s.url
#             res.append(jsn)
#         elif sharetype == 'rent' and ltype == 'listing2':
#             jsn['mls'] = s.listingid
#             jsn['listingname'] = s.listingname
#             jsn['listingtype'] = 'rent'
#             jsn['addr'] = s.listingname
#             jsn['price'] = s.price
#             jsn['areas'] = s.areas if s.areas.strip() <> '' else '-- sqft.'
#             jsn['cityname'] = s.cityname
#             jsn['housetype'] = s.housetype
#             jsn['visit'] = s.visit
#             jsn['good'] = s.good
#             jsn['date'] = s.datadate.strftime('%Y-%m-%d')
#             jsn['htmlid'] = s.url
#             res.append(jsn)
#             
#     r = HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
#     r["Access-Control-Allow-Origin"] = "*"
#     return r
# 
# def get_mysite_spread(request):
#     page = int(request.GET.get('page','1')) * 4
#     od = Systemorder.objects.filter(status='completed',ordertype='mysite')
#     lastpage = int(ceil(len(od)/4.0))
#     userids = [o.dataid for o in od[page-4:page]]
#     res = []
#     for userid in userids:
#         ui = Userinfo.objects.get(userid=userid)
#         jsn = {}
#         jsn['userid'] = ui.userid
#         jsn['username'] = ui.username
#         jsn['usercity'] = ui.usercity
#         jsn['corp'] = ui.corp
#         jsn['note'] = ui.note
#         jsn['auth'] = 1 if ui.creditcard <> '' else 0
#         jsn['img'] = Userimage.objects.get(userid=userid,imgtype='head').img.url
#         jsn['wechat'] = Userimage.objects.get(userid=userid,imgtype='wechat').img.url
#         jsn['lastpage'] = lastpage
#         res.append(jsn)
#     r = HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
#     r["Access-Control-Allow-Origin"] = "*"
#     return r


def parse_conditions(items):
    """country-province-group-city-county-listingtype-housetype-bedroom-price-page"""
    cons = items.split('-')
    if len(cons) != 10:
        return False
    cdt = {}
    cdt['country'] = cons[0]
    cdt['prov'] = cons[1]
    cdt['group'] = cons[2]
    cdt['city'] = cons[3]
    cdt['county'] = cons[4]

    if cdt['county'] != 'all':
        cdt['dist'] = cdt['county']
        for row in MySql.sel_table(
                "select countyname from app.t99_cityname where countyid='%s' " %
                cdt['county']):
            cdt['dist_cn'] = row[0]
    elif cdt['city'] != 'all':
        cdt['dist'] = cdt['city']
        for row in MySql.sel_table(
                "select cityname from app.t99_cityname where cityid='%s' " %
                cdt['city']):
            cdt['dist_cn'] = row[0]
    elif cdt['group'] != 'all':
        cdt['dist'] = cdt['group']
        for row in MySql.sel_table(
                "select groupname from app.t99_cityname where groupid='%s' " %
                cdt['group']):
            cdt['dist_cn'] = row[0]
    elif cdt['prov'] != 'all':
        cdt['dist'] = cdt['prov']
        for row in MySql.sel_table(
                "select provname from app.t99_cityname where provid='%s' " %
                cdt['prov']):
            cdt['dist_cn'] = row[0]
    elif cdt['country'] != 'all':
        cdt['dist'] = cdt['country']
        for row in MySql.sel_table(
                "select countryname from app.t99_cityname where countryid='%s' " %
                cdt['country']):
            cdt['dist_cn'] = row[0]
    else:
        cdt['dist'] = ''
        cdt['dist_cn'] = ''

    cdt['listingtype'] = cons[5]
    if cdt['listingtype'] == 'new':
        cdt['listingtype_cn'] = '新房'
    elif cdt['listingtype'] == 'sale':
        cdt['listingtype_cn'] = '二手房'
    elif cdt['listingtype'] == 'rent':
        cdt['listingtype_cn'] = '租房'
    else:
        cdt['listingtype_cn'] = ''
    cdt['housetype'] = cons[6]
    cdt['housetype_cn'] = '其他'
    for row in MySql.sel_table(
            "select typename from app.t99_housetype where housetype='%s' " %
            cons[6]):
        cdt['housetype_cn'] = row[0]

    cdt['bedroom'] = cons[7]
    # cdt['toilet'] = cons[8]
    cdt['price'] = cons[8]
    if cdt['price'] == '3050':
        cdt['price_cn'] = '$30万-$50万'
    elif cdt['price'] == '50100':
        cdt['price_cn'] = '$50万-$100万'
    elif cdt['price'] == '100150':
        cdt['price_cn'] = '$100万-$150万'
    elif cdt['price'] == '150200':
        cdt['price_cn'] = '$150万-$200万'
    elif cdt['price'] == '200300':
        cdt['price_cn'] = '$200万-$300万'
    elif cdt['price'] == '300400':
        cdt['price_cn'] = '$300万-$400万'
    elif cdt['price'] == '400':
        cdt['price_cn'] = '$400万以上'
    else:
        cdt['price_cn'] = ''

    cdt['page'] = cons[9]
    return cdt


def make_sql(cdt):
    sql = """
            SELECT a.*
            FROM app.app_listing a
            LEFT JOIN app.`t99_cityname` b
            ON a.cityname = b.srcdata
            LEFT JOIN app.`t99_housetype` c
            ON a.housetype = c.srcdata
            where 1=1
                """
    sql2 = """
            SELECT count(1) as cnt
            FROM app.app_listing a
            LEFT JOIN app.`t99_cityname` b
            ON a.cityname = b.srcdata
            LEFT JOIN app.`t99_housetype` c
            ON a.housetype = c.srcdata
            where 1=1
                """
    where = " and datadate < '2019-05-01 00:00:00'"
    if cdt['country'] != 'all':
        where += " and b.countryid = '%s' " % cdt['country']
    if cdt['prov'] != 'all':
        where += " and b.provid = '%s' " % cdt['prov']
    if cdt['group'] != 'all':
        where += " and b.groupid = '%s' " % cdt['group']
    if cdt['city'] != 'all':
        where += " and b.cityid = '%s' " % cdt['city']
    if cdt['county'] != 'all':
        where += " and b.countyid = '%s' " % cdt['county']
    if cdt['listingtype'] != 'all':
        pass
    if cdt['housetype'] != 'all':
        where += " and c.housetype = '%s' " % cdt['housetype']
    if cdt['bedroom'] != 'all':
        where += " and CAST(a.bedroom AS SIGNED)>=%s " % cdt['bedroom']
    #     if cdt['toilet'] != 'all':
    #         where += " and CAST(a.toilet AS SIGNED)>=%s " % cdt['toilet']

    # 价格区间
    if cdt['price'] == '3050':
        where += " and CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) BETWEEN 300000 AND 500000"
    elif cdt['price'] == '50100':
        where += " and CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) BETWEEN 500000 AND 1000000"
    elif cdt['price'] == '100150':
        where += " and CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) BETWEEN 1000000 AND 1500000"
    elif cdt['price'] == '150200':
        where += " and CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) BETWEEN 1500000 AND 2000000"
    elif cdt['price'] == '200300':
        where += " and CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) BETWEEN 2000000 AND 3000000"
    elif cdt['price'] == '300400':
        where += " and CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) BETWEEN 3000000 AND 4000000"
    elif cdt['price'] == '400':
        where += " and CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) > 4000000"

    limit = " order by a.datadate desc limit %s,%s" % (
        int(cdt['page']) * 10 - 10, 10)
    return sql + where + limit, sql2 + where


def get_listings(request, items):
    cdt = parse_conditions(items)
    if not cdt:
        cdt = {}
        cdt['country'] = 'all'
        cdt['prov'] = 'all'
        cdt['group'] = 'all'
        cdt['city'] = 'all'
        cdt['county'] = 'all'
        cdt['listingtype'] = 'all'
        cdt['housetype'] = 'all'
        cdt['bedroom'] = 'all'
        # cdt['toilet'] = 'all'
        cdt['price'] = 'all'
        cdt['page'] = '1'
    cities = {}
    counties = {}
    if cdt['group'] != 'all':
        cities = get_cities(cdt['group'])
    if cdt['city'] != 'all':
        counties = get_counties(cdt['city'])

    ls = Listing.objects.raw(make_sql(cdt)[0])

    for i in MySql.sel_table(make_sql(cdt)[1]):
        cnt = int(i[0])

    maxpage = int(ceil(cnt / 10.0))

    res = []
    for l in ls:
        limg = Listingimg.objects.filter(listingid=l.listingid,
                                         imgtype='listing1')
        jsn = {}
        jsn['mls'] = l.listingid
        jsn['price'] = l.price
        jsn['addr'] = l.cityname
        jsn['bedroom'] = l.bedroom if l.bedroom.strip() <> '' else '0'
        jsn['toilet'] = l.toilet[:1] if l.toilet.strip() <> '' else '0'
        jsn['areas'] = l.areas if l.areas.strip() <> '' else '-- sqft.'
        jsn['date'] = l.datadate.strftime('%Y-%m-%d')
        jsn['visit'] = l.visit
        jsn['good'] = l.good
        jsn['img'] = 'http://' + request.META[
            'HTTP_HOST'] + '/static/img/def_listingimg5.jpg'
        for i in limg:
            jsn['img'] = i.img.url
            break
        res.append(jsn)
    r = render_to_response('web/houselist.html',
                           {'listings': res, 'currpage': cdt['page'],
                            'pages': range(1, maxpage + 1),
                            'lastpage': maxpage, 'cdt': cdt
                               , 'cities': cities, 'counties': counties,
                            'cnt': cnt})
    r["Access-Control-Allow-Origin"] = "*"
    return r


def get_listings_redirect(request, items):
    return redirect("/web/houses/%s" % items, permanent=True)


def call_agent(request):
    userid = request.POST.get('userid')
    name = request.POST.get('name')
    tel = request.POST.get('tel')
    msg = request.POST.get('msg')
    mls = request.POST.get('mls')
    info = {}
    info['userid'] = userid
    info['name'] = name
    info['tel'] = tel
    info['msg'] = msg
    info['mls'] = mls
    send_usermsg(info)
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='callagent',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=userid, htmlid=name)
    his.save()
    return HttpResponse('ok')


def agent_page_redirect(request):
    userid = request.GET.get('userid', '')
    return redirect('/web/agent/?userid=%s' % userid, permanent=True)


def agent_page(request, uid):
    try:
        ui = agent_info.objects.get(id=uid)
        if ui.userid in ('amir@amirmiri.com', 'juliewang321@hotmail.com'):
            return redirect('/')
        if agent_auth.objects.filter(userid=ui.userid, status='paid',
                                     service='vip'):
            return redirect('/web/agent2/%s' % ui.id, permanent=True)
    except agent_info.DoesNotExist:
        return HttpResponse('no user!')
    userinfo = {}
    userinfo['usercity'] = ui.city if ui.city != '' else '加拿大'
    userinfo['username'] = ui.username
    userinfo['userid'] = ui.userid
    userinfo['corp'] = ui.corp
    userinfo['address'] = ui.address
    userinfo['email'] = ui.email
    userinfo['postid'] = ui.postid
    userinfo['tel'] = ui.tel
    userinfo['note'] = ui.note
    userinfo['siteurl'] = ui.website
    userinfo['assistant'] = ui.username2
    userinfo['assistanttel'] = ui.tel2
    userinfo['visit'] = Access_hitory.objects.filter(htmltype='agenthome',
                                                     userid=ui.userid).count()
    userinfo['selfintro'] = ui.selfintro.strip()
    userinfo['corpintro'] = ui.corpintro.strip()
    userinfo['teamintro'] = ui.teamintro.strip()
    userinfo['selfintro_cn'] = ui.selfintro_cn.strip()
    userinfo['corpintro_cn'] = ui.corpintro_cn.strip()
    userinfo['teamintro_cn'] = ui.teamintro_cn.strip()
    userinfo['wechat'] = ui.qrcode.url
    userinfo['team'] = []
    userinfo['history'] = []
    userinfo[
        'star'] = 5  # int(float(MySql.data_integrity(ui.userid).replace('%','')))/20
    userinfo['identity'] = '1' if agent_auth.objects.filter(userid=ui.userid,
                                                            status='paid',
                                                            service='auth') else '0'
    userinfo['head'] = ui.head.url
    uimg = agent_img.objects.filter(userid=ui.userid)
    for i in uimg:
        if i.imgtype == 'agent':
            userinfo['team'].append(i.img.url)
            userinfo['history'].append(i.img.url)
    if len(userinfo.get('team')) == 0:
        userinfo['team'].append(
            'http://www.realtoraccess.com/static/web/img/def_selfimg.png')
    if len(userinfo.get('history')) == 0:
        userinfo['history'].append(
            'http://www.realtoraccess.com/static/web/img/def_selfimg.png')

    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='agenthome',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=ui.userid)
    his.save()
    return render_to_response('web/agenthome.html', {'userinfo': userinfo})


def news_shared(request):
    userid = request.GET.get('userid', '')
    sr = Sharesite.objects.filter(userid=userid, sharetype='article').order_by(
        '-sharetime')
    articles = []
    for s in sr:
        atc = Article_info.objects.get(articleid=s.dataid)
        tmp = {}
        tmp['id'] = atc.id
        tmp['title'] = atc.title
        tmp['date'] = s.sharetime.strftime('%Y-%m-%d')
        tmp['img'] = atc.img.url
        tmp['visit'] = atc.look
        articles.append(tmp)

    res = {}
    res['articles'] = articles
    res['page'] = int(ceil(len(articles) / 4.0))
    return HttpResponse(json.dumps(res, indent=2, ensure_ascii=False))


def agent_list_page(request, items):
    agents = agent_info.objects.filter(active='1')
    agentcnt = len(agents)
    lastpage = int(ceil(agentcnt / 8.0))
    pages = [i + 1 for i in range(lastpage)]

    if len(items.split('-')) == 3:
        (orderby, ad, page) = items.split('-')
    else:
        (orderby, ad, page) = '0', '1', '1'
    order = ['0-0-1', '1-0-1', '2-0-1']
    order[int(orderby)] = '%s-%s-%s' % (orderby, 1 if ad == '0' else '0', 1)

    print len(items.split('-'))
    print items
    # 默认排序，按经纪付费认证情况
    if len(items.split('-')) == 1:
        try:
            page = int(items.split('-')[0])
        except ValueError:
            page = 1
        agents = agent_info.objects.raw("""
                    SELECT a.* 
                    FROM app.`web_agent_info` a
                    LEFT JOIN
                    (
                    SELECT userid,SUM(CASE WHEN service = 'auth' THEN 9
                                                WHEN service = 'vip' THEN 8
                                                ELSE 0 END) AS v
                    FROM app.`web_agent_auth` GROUP BY userid
                    ) b
                    ON a.`userid` = b.userid
                    where a.active = '1'
                    ORDER BY CASE WHEN b.v IS NULL THEN 0 ELSE b.v END DESC,
                    a.`datadate` DESC,
                    CASE WHEN a.username <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.tel <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.note <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.website <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.address <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.selfintro <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.corp <> '' THEN 1 ELSE 0 END+
                    CASE WHEN a.head <> 'agentimgs/def_head.png' THEN 1 ELSE -99 END+
                    CASE WHEN a.qrcode <> 'agentimgs/def_qrcode.png' THEN 1 ELSE 0 END+
                    CASE WHEN a.username2 <> '' THEN 1 ELSE 0 END DESC
                    limit %s,%s
                    """ % (int(page) * 8 - 8, 8))

    # 按信息完整度排序
    elif orderby == '0':
        agents = agent_info.objects.raw("""
                    SELECT *
                    FROM app.`web_agent_info`
                    where active = '1'
                    ORDER BY
                    CASE WHEN username <> '' THEN 1 ELSE 0 END+
                    CASE WHEN tel <> '' THEN 1 ELSE 0 END+
                    CASE WHEN email <> '' THEN 1 ELSE 0 END+
                    CASE WHEN note <> '' THEN 1 ELSE 0 END+
                    CASE WHEN website <> '' THEN 1 ELSE 0 END+
                    CASE WHEN address <> '' THEN 1 ELSE 0 END+
                    CASE WHEN selfintro <> '' THEN 1 ELSE 0 END+
                    CASE WHEN corpintro <> '' THEN 1 ELSE 0 END+
                    CASE WHEN teamintro <> '' THEN 1 ELSE 0 END+
                    CASE WHEN corp <> '' THEN 1 ELSE 0 END+
                    CASE WHEN postid <> '' THEN 1 ELSE 0 END+
                    CASE WHEN head <> 'agentimgs/def_head.png' THEN 1 ELSE -99 END+
                    CASE WHEN qrcode <> 'agentimgs/def_qrcode.png' THEN 1 ELSE 0 END+
                    CASE WHEN logo <> 'agentimgs/def_logo.png' THEN 1 ELSE 0 END+
                    CASE WHEN username2 <> '' THEN 1 ELSE 0 END+
                    CASE WHEN tel2 <> '' THEN 1 ELSE 0 END+
                    CASE WHEN email2 <> '' THEN 1 ELSE 0 END+
                    CASE WHEN head2 <> 'agentimgs/def_head.png' THEN 1 ELSE 0 END+
                    CASE WHEN qrcode2 <> 'agentimgs/def_qrcode.png' THEN 1 ELSE 0 END+
                    CASE WHEN country <> '' THEN 1 ELSE 0 END+
                    CASE WHEN prov <> '' THEN 1 ELSE 0 END+
                    CASE WHEN `group` <> '' THEN 1 ELSE 0 END+
                    CASE WHEN city <> '' THEN 1 ELSE 0 END+
                    CASE WHEN county <> '' THEN 1 ELSE 0 END+
                    CASE WHEN fname <> '' THEN 1 ELSE 0 END+
                    CASE WHEN lname <> '' THEN 1 ELSE 0 END %s
                    limit %s,%s
                    """ % (
            'desc' if ad == '0' else 'asc', int(page) * 8 - 8, 8))

    # 发布房源数量
    elif orderby == '1':
        agents = agent_info.objects.raw("""
                    SELECT a.*
                    FROM app.`web_agent_info` a
                    LEFT JOIN
                    (SELECT userid,COUNT(*) AS cnt FROM app.`singlepage_tokens` GROUP BY userid) b
                    ON a.userid = b.userid
                    where a.active = '1'
                    ORDER BY IFNULL(b.cnt,0) %s
                    limit %s,%s
                    """ % (
            'desc' if ad == '0' else 'asc', int(page) * 8 - 8, 8))

    # 发布房源价格
    elif orderby == '2':
        agents = agent_info.objects.raw("""
                    SELECT a.*
                    FROM app.`web_agent_info` a
                    LEFT JOIN
                    (SELECT cc.userid,AVG(CAST(REPLACE(REPLACE(bb.price,'$',''),',','') AS SIGNED)) AS p 
                    FROM app.`singlepage_listing_for_sp` bb
                    INNER JOIN app.`singlepage_tokens` cc
                    ON bb.token = cc.token
                    GROUP BY cc.userid
                    ) b
                    ON a.userid = b.userid
                    where a.active = '1'
                    ORDER BY IFNULL(b.p,0) %s
                    limit %s,%s
                    """ % (
            'desc' if ad == '0' else 'asc', int(page) * 8 - 8, 8))

    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='agentlist',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'))
    his.save()
    return render_to_response('web/agentlisting.html',
                              {'cnt': agentcnt, 'lastpage': lastpage,
                               'pages': pages, 'agents': agents, 'order': order,
                               'currorder': orderby, 'currad': ad,
                               'currpage': page,
                               'deforder': 1 if len(
                                   items.split('-')) == 1 else 0})


def search_listing(request):
    q = request.GET.get('q', '').strip()
    qtype = request.GET.get('qtype')
    res = []
    if qtype == 'listing1':
        try:
            ls = Listing.objects.get(listingid=q)
        except Listing.DoesNotExist:
            return render_to_response('web/search.html', {'res': res})
        jsn = {}
        jsn['mls'] = ls.listingid
        jsn['price'] = ls.price
        jsn['addr'] = ls.cityname
        jsn['bedroom'] = ls.bedroom if ls.bedroom.strip() <> '' else '0'
        jsn['toilet'] = ls.toilet[:1] if ls.toilet.strip() <> '' else '0'
        jsn['areas'] = ls.areas if ls.areas.strip() <> '' else '-- sqft.'
        jsn['date'] = ls.datadate.strftime('%Y-%m-%d')
        jsn['visit'] = ls.visit
        jsn['good'] = ls.good
        jsn['type'] = 'listing1'
        limg = Listingimg.objects.filter(listingid=ls.listingid,
                                         imgtype='listing1')
        jsn['img'] = 'http://' + request.META[
            'HTTP_HOST'] + '/static/img/def_listingimg5.jpg'
        for i in limg:
            jsn['img'] = i.img.url
            break
        res.append(jsn)
    else:
        ls = Listing2.objects.filter(listingname__icontains=q)
        for l in ls:
            jsn = {}
            jsn['mls'] = l.listingid
            jsn['price'] = l.price1
            jsn['addr'] = l.cityname
            jsn['bedroom'] = '--'
            jsn['toilet'] = '--'
            jsn['areas'] = l.areas if l.areas.strip() <> '' else '-- sqft.'
            jsn['date'] = l.datadate.strftime('%Y-%m-%d')
            jsn['visit'] = l.visit
            jsn['good'] = l.good
            jsn['type'] = 'listing2'
            limg = Listingimg.objects.filter(listingid=l.listingid,
                                             imgtype='listing2')
            jsn['img'] = 'http://' + request.META[
                'HTTP_HOST'] + '/static/img/def_listingimg5.jpg'
            for i in limg:
                jsn['img'] = i.img.url
                break
            res.append(jsn)
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='findhouse',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        htmlid=q)
    his.save()
    return render_to_response('web/search.html', {'res': res})


def save_comment(request):
    comm = request.POST.get('comment', '').strip()
    userid = request.POST.get('userid', '')
    ip = request.META['REMOTE_ADDR']
    sc = Sitecomment(htmlid=userid, userid=ip, usercomment=comm,
                     commtype='agent')
    sc.save()
    return HttpResponse('ok')


def get_comments(request):
    userid = request.GET.get('userid', '')
    page = int(request.GET.get('page', '1')) * 10
    sc = Sitecomment.objects.filter(htmlid=userid, commtype='agent')[
         page - 10:page]
    jsn = []
    for s in sc:
        tmp = {}
        tmp['commenter'] = s.userid
        tmp['comment'] = s.usercomment
        tmp['commdate'] = s.commtime.strftime('%Y-%m-%d')
        jsn.append(tmp)
    return HttpResponse(json.dumps(jsn, indent=2, ensure_ascii=False))


def get_share_history(request):
    page = int(request.GET.get('page', '1')) * 4
    userid = request.GET.get('userid', '')

    tks = [tk.token for tk in Tokens.objects.filter(userid=userid)]
    ll1 = Listing_for_sp.objects.filter(token__in=tks)

    ll2 = Listing.objects.filter(
        listingid__in=(
            'r2265452', 'r2265459', 'r2261675', 'r2263196', 'r2260737',
            'r2263429',
            'r2261163', 'r2261920'))
    jsn = []
    for l in ll1:
        if l.salestatus == 'invalid':
            continue
        tmp = {}
        tmp['mls'] = l.listingid
        tmp['price'] = l.price
        tmp['cityname'] = l.cityname
        tmp['bedroom'] = l.bedroom if l.bedroom.strip() <> '' else '0'
        tmp['toilet'] = l.toilet[:1] if l.toilet.strip() <> '' else '0'
        tmp['areas'] = l.areas if l.areas.strip() <> '' else '-- sqft.'
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['housetype'] = l.housetype
        tmp['visit'] = l.visit
        tmp['good'] = l.good
        #         tmp['lastpage'] = lastpage
        tmp['href'] = l.url
        limg = Listingimg.objects.filter(listingid=l.listingid,
                                         imgtype='listing1')
        tmp['img'] = 'http://' + request.META[
            'HTTP_HOST'] + '/static/img/def_listingimg5.jpg'

        for i in limg:
            tmp['img'] = i.img.url
            break
        jsn.append(tmp)
    for l in ll2:
        tmp = {}
        tmp['mls'] = l.listingid
        tmp['price'] = l.price
        tmp['cityname'] = l.cityname
        tmp['bedroom'] = l.bedroom if l.bedroom.strip() <> '' else '0'
        tmp['toilet'] = l.toilet[:1] if l.toilet.strip() <> '' else '0'
        tmp['areas'] = l.areas if l.areas.strip() <> '' else '-- sqft.'
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['housetype'] = l.housetype
        tmp['visit'] = l.visit
        tmp['good'] = l.good
        #         tmp['lastpage'] = lastpage
        tmp['href'] = 'http://' + request.META[
            'HTTP_HOST'] + '/web/listing1/%s/' % l.listingid
        limg = Listingimg.objects.filter(listingid=l.listingid,
                                         imgtype='listing1')
        tmp['img'] = 'http://' + request.META[
            'HTTP_HOST'] + '/static/img/def_listingimg5.jpg'

        for i in limg:
            tmp['img'] = i.img.url
            break
        jsn.append(tmp)

    lastpage = int(ceil((len(jsn)) / 4.0))
    for j in jsn:
        j['lastpage'] = lastpage
    jsn = jsn[page - 4:page]

    return HttpResponse(json.dumps(jsn, indent=2, ensure_ascii=False))


def agent_list(request):
    rule = request.GET.get('rule', '')
    order = request.GET.get('order', 'desc')
    page = int(request.GET.get('page', '1')) * 4

    if rule == 'integrity':
        ui = Userinfo.objects.raw("""SELECT *,FORMAT((CASE WHEN LENGTH(a.username) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.usercity) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.tel) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.note) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.email) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.siteurl) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.assistant) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.address) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.selfintro) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.teamintro) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.corpintro) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.agentid) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.creaid) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.creditcard) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.assistanttel) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.postid) > 0 THEN 1 ELSE 0 END+
                                    CASE WHEN LENGTH(a.corp) > 0 THEN 1 ELSE 0 END)/17,2)*100 AS integrity
                                    FROM app.app_userinfo a
                                    WHERE a.role = 'agent'
                                    and a.userid not in
                                    ('514430840@qq.com',
                                    'wechat',
                                    '932320908@qq.com',
                                    '1021731713@qq.com',
                                    '452144286@qq.com',
                                    '2516435261@qq.com',
                                    'diao.xc@qq.com',
                                    'cluentservice@realtoraccess.com')
                                    ORDER BY integrity %s
                                    LIMIT %s,%s""" % (order, page - 4, 4))
        jsn = []
        for u in ui:
            tmp = {}
            tmp['id'] = u.id
            tmp['userid'] = u.userid
            tmp['username'] = u.username
            tmp['usercity'] = u.usercity
            tmp['tel'] = u.tel
            tmp['email'] = u.email
            tmp['note'] = u.note
            tmp['corp'] = u.corp
            tmp['selfinfo'] = u.selfintro
            tmp['star'] = int(
                float(MySql.data_integrity(u.userid).replace('%', ''))) / 20
            tmp['head'] = Userimage.objects.get(userid=u.userid,
                                                imgtype='head').img.url
            jsn.append(tmp)
        return HttpResponse(json.dumps(jsn, indent=2, ensure_ascii=False))

    elif rule == 'sharecnt':
        ui = Userinfo.objects.raw("""SELECT a.*,IFNULL(b.cnt,0) AS cnt
                                    FROM app_userinfo a
                                    LEFT JOIN
                                    (SELECT userid,COUNT(*) AS cnt FROM app_sharesite WHERE sharetype = 'listing1' GROUP BY userid) b
                                    ON a.userid = b.userid
                                    WHERE a.`role` = 'agent'
                                    and a.userid not in
                                    ('514430840@qq.com',
                                    'wechat',
                                    '932320908@qq.com',
                                    '1021731713@qq.com',
                                    '452144286@qq.com',
                                    '2516435261@qq.com',
                                    'diao.xc@qq.com',
                                    'cluentservice@realtoraccess.com')
                                    ORDER BY cnt %s
                                    LIMIT %s,%s""" % (order, page - 4, 4))
        jsn = []
        for u in ui:
            tmp = {}
            tmp['id'] = u.id
            tmp['userid'] = u.userid
            tmp['username'] = u.username
            tmp['usercity'] = u.usercity
            tmp['tel'] = u.tel
            tmp['email'] = u.email
            tmp['note'] = u.note
            tmp['corp'] = u.corp
            tmp['selfinfo'] = u.selfintro
            tmp['star'] = int(
                float(MySql.data_integrity(u.userid).replace('%', ''))) / 20
            tmp['head'] = Userimage.objects.get(userid=u.userid,
                                                imgtype='head').img.url
            jsn.append(tmp)
        return HttpResponse(json.dumps(jsn, indent=2, ensure_ascii=False))

    elif rule == 'shareprice':
        ui = Userinfo.objects.raw("""SELECT a.*,IFNULL(b.prc,0) AS prc
                                    FROM app_userinfo a
                                    LEFT JOIN
                                    (SELECT a.userid,AVG(CAST(REPLACE(REPLACE(b.price,'$',''),',','') AS SIGNED)) AS prc 
                                     FROM app_sharesite a
                                     INNER JOIN app_listing b
                                     ON a.dataid = b.listingid
                                     AND a.sharetype = 'listing1'
                                     GROUP BY a.userid) b
                                    ON a.userid = b.userid
                                    WHERE a.`role` = 'agent'
                                    and a.userid not in
                                    ('514430840@qq.com',
                                    'wechat',
                                    '932320908@qq.com',
                                    '1021731713@qq.com',
                                    '452144286@qq.com',
                                    '2516435261@qq.com',
                                    'diao.xc@qq.com',
                                    'cluentservice@realtoraccess.com')
                                    ORDER BY prc %s
                                    LIMIT %s,%s""" % (order, page - 4, 4))
        jsn = []
        for u in ui:
            tmp = {}
            tmp['id'] = u.id
            tmp['userid'] = u.userid
            tmp['username'] = u.username
            tmp['usercity'] = u.usercity
            tmp['tel'] = u.tel
            tmp['email'] = u.email
            tmp['note'] = u.note
            tmp['corp'] = u.corp
            tmp['selfinfo'] = u.selfintro
            tmp['star'] = int(
                float(MySql.data_integrity(u.userid).replace('%', ''))) / 20
            tmp['head'] = Userimage.objects.get(userid=u.userid,
                                                imgtype='head').img.url
            jsn.append(tmp)
        return HttpResponse(json.dumps(jsn, indent=2, ensure_ascii=False))
    else:
        return HttpResponse('illegal param')


def find_agent(request):
    searchof = request.GET.get('searchof', '')
    try:
        ui = [agent_info.objects.get(userid=searchof, active='1')]
    except agent_info.DoesNotExist:
        ui = agent_info.objects.filter(username__icontains=searchof, active='1')
    jsn = []
    for u in ui:
        tmp = {}
        tmp['id'] = u.id
        tmp['userid'] = u.userid
        tmp['username'] = u.username
        tmp['usercity'] = u.city if u.city != '' else '加拿大'
        tmp['tel'] = u.tel
        tmp['email'] = u.email
        tmp['note'] = u.note
        tmp['corp'] = u.corp
        tmp['selfinfo'] = u.selfintro
        tmp['star'] = 5
        tmp['head'] = u.head.url
        jsn.append(tmp)
    return HttpResponse(json.dumps(jsn, indent=2, ensure_ascii=False))


def get_some_agent(request):
    mls = request.GET.get('mls', '').lower()
    userid = request.GET.get('userid', '')
    chgrule = {}
    chgrule['r2301799'] = ['yaletownrealtor@gmail.com', 'plegree@gmail.com']
    chgrule['r2287114'] = ['mwtsang@aol.com', 'plegree@gmail.com']
    print mls, userid
    if chgrule.get(mls) is not None:
        try:
            rcmd = chgrule.get(mls)[chgrule.get(mls).index(userid) + 1]
        except (ValueError, IndexError):
            rcmd = chgrule.get(mls)[0]
        agent = agent_info.objects.get(userid=rcmd)
    else:
        ui = agent_info.objects.filter(active='1')
        i = random.randint(0, len(ui) - 1)
        agent = ui[i]
    info = {}
    info['userid'] = agent.userid
    info['username'] = agent.username
    info['usercity'] = agent.city if agent.city != '' else '加拿大'
    info['corp'] = agent.corp
    info['tel'] = agent.tel
    info['head'] = agent.head.url
    return HttpResponse(json.dumps(info, indent=2, ensure_ascii=False))


def map_listings(request):
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='housemap',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'))
    his.save()
    return render_to_response('web/bootfind.html')


def map_listings_m(request):
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='openhouse',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'))
    his.save()
    res = render_to_response('web/map.html')
    res['X-Frame-Options'] = 'ALLOWALL'
    return res


def get_area_listings(request):
    print request.GET
    country = request.GET.get('country', '')
    prov = request.GET.get('prov', '')
    group = request.GET.get('group', '')
    city = request.GET.get('city', '')
    housetype = request.GET.get('housetype', '')
    bgndate = request.GET.get('bgndate')
    enddate = request.GET.get('enddate')

    salestatus = {}
    salestatus['saling'] = 'no'
    salestatus['rent'] = 'rent'
    salestatus['presale'] = 'presale'

    sql = """
            select a.* from 
            app.singlepage_listing_for_sp a
            left join app.t99_cityname b
            on a.distid = b.srcdata
            LEFT JOIN app.`singlepage_openhouse` d
            ON a.`listingid` = d.`listingid`
            where 1=1
            and a.salestatus <> 'yes'
            and a.mapspread = '1'
            """
    if country != "":
        sql += "and b.countryid = '%s' " % country
    if prov != "":
        sql += "and b.provid = '%s' " % prov
    if group != "":
        sql += "and b.groupid = '%s' " % group
    if city != "":
        sql += "and b.cityid = '%s' " % city
    if housetype != "":
        sql += "and a.salestatus = '%s' " % salestatus.get(housetype)
    if bgndate and not enddate:
        bgndate = bgndate[0:8]
        sql += "and (DATE_FORMAT(d.bgndate1,'%%%%Y%%%%m%%%%d') = '%s' OR DATE_FORMAT(d.bgndate2,'%%%%Y%%%%m%%%%d') = '%s') " % (
            bgndate, bgndate)
    elif enddate and not bgndate:
        enddate = enddate[0:8]
        sql += "and (DATE_FORMAT(d.enddate1,'%%%%Y%%%%m%%%%d') = '%s' OR DATE_FORMAT(d.enddate2,'%%%%Y%%%%m%%%%d') = '%s') " % (
            enddate, enddate)
    elif bgndate and enddate:
        bgndate = bgndate[0:8]
        enddate = enddate[0:8]
        sql += """
        and ((DATE_FORMAT(d.bgndate1,'%%%%Y%%%%m%%%%d') >= '%s' AND DATE_FORMAT(d.enddate1,'%%%%Y%%%%m%%%%d') <= '%s')
        or (DATE_FORMAT(d.bgndate2,'%%%%Y%%%%m%%%%d') >= '%s' AND DATE_FORMAT(d.enddate2,'%%%%Y%%%%m%%%%d') <= '%s')) """ % (
            bgndate, enddate, bgndate, enddate)

    sql += " order by datadate desc"

    res = []
    print sql
    tmp = Listing_for_sp.objects.raw(sql)
    #     tmp = []
    #     for sp in sps:
    #         tmp.append([sp.listingid,sp.url])
    for l in tmp:
        imgs = Listingimg.objects.filter(listingid=l.listingid,
                                         imgtype='listing1')
        tmp = {}

        if imgs:
            for img in imgs:
                tmp['img'] = img.img.url
                break
        else:
            continue
        tmp['listingid'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['lat'] = l.lat
        tmp['lng'] = l.lng
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['bedroom'] = l.bedroom
        tmp['toilet'] = l.toilet
        tmp['areas'] = l.areas
        tmp['housetype'] = l.housetype
        res.append(tmp)

    return HttpResponse(json.dumps(res, indent=2, ensure_ascii=False))


def to_get_countries(request):
    return HttpResponse(
        json.dumps(get_countries(), indent=2, ensure_ascii=False))


def to_get_provs(request):
    countryid = request.GET.get('countryid', '')
    return HttpResponse(
        json.dumps(get_provs(countryid), indent=2, ensure_ascii=False))


def to_get_groups(request):
    provid = request.GET.get('provid', '')
    return HttpResponse(
        json.dumps(get_groups(provid), indent=2, ensure_ascii=False))


def to_get_cities(request):
    groupid = request.GET.get('groupid', '')
    return HttpResponse(
        json.dumps(get_cities(groupid), indent=2, ensure_ascii=False))


def to_get_counties(request):
    cityid = request.GET.get('cityid', '')
    return HttpResponse(
        json.dumps(get_counties(cityid), indent=2, ensure_ascii=False))


def sign_up(request):
    userid = request.POST.get('userid', '')
    passwd1 = request.POST.get('passwd1', '')
    passwd2 = request.POST.get('passwd2', '')
    frm = request.POST.get('from', '')

    MySql.run_sql(
        "insert into app.web_signup_channel values('%s','%s',now())" % (
            userid, frm))

    if passwd1 != passwd2:
        return HttpResponse(
            get_res_info('1', 'Incorrect password or user name！'))
    if User.objects.all().filter(username=userid):
        return HttpResponse(
            get_res_info('2', 'Email already exits：%s' % userid))
    u = User.objects.create_user(userid, userid, passwd1)
    u.save()
    agt = agent_info(userid=userid, email=userid, logo='agentimgs/def_logo.png',
                     head='agentimgs/def_head.png',
                     head2='agentimgs/def_head.png'
                     , qrcode='agentimgs/def_qrcode.png',
                     qrcode2='agentimgs/def_qrcode.png')
    agt.save()
    user = authenticate(username=userid, password=passwd1)
    login(request, user)
    try:
        welcome_for_signup(userid)
    except:
        print '注册成功，发邮件失败！'
    if frm != '':
        mail_api('G', frm, userid, '', '')
        third_party_signup(userid)
    return HttpResponse(get_res_info())


def sign_in(request):
    userid = request.POST.get('userid', '')
    passwd = request.POST.get('passwd', '')
    try:
        User.objects.get(username=userid)
    except User.DoesNotExist:
        return HttpResponse(get_res_info('1', ' Account does not exit!'))
    user = authenticate(username=userid, password=passwd)
    if user is not None:
        if user.is_active:
            login(request, user)
            u = agent_info.objects.get(userid=userid)
            resinfo = {}
            resinfo['rescode'] = '0'
            resinfo['resdesc'] = '成功'
            resinfo['redirect'] = '/web/agent2/14'
            ret = HttpResponse(
                json.dumps(resinfo, ensure_ascii=False, indent=2))
            ret.set_cookie('id', userid, max_age=604800)
            ret.set_cookie('username', u.username, max_age=604800)
            if hasattr(u.head, 'url'):
                ret.set_cookie('head', u.head.url, max_age=604800)
            else:
                ret.set_cookie('head', '/static/web/img/defhead.png',
                               max_age=604800)
            return ret
        else:
            return HttpResponse(get_res_info('3', 'User invalid!'))
    else:
        return HttpResponse(get_res_info('2', 'Password invalid!'))


def log_out(request):
    logout(request)
    return redirect('/web/page/signin/')


def update_agent_info(request):
    print request.POST
    userid = request.POST.get('userid')
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    tel = request.POST.get('tel')
    email = request.POST.get('email')
    address = request.POST.get('address')
    corp = request.POST.get('corp')
    note = request.POST.get('note')
    website = request.POST.get('website')
    postid = request.POST.get('postid')
    username2 = request.POST.get('username2')
    tel2 = request.POST.get('tel2')
    email2 = request.POST.get('email2')
    selfintro = request.POST.get('selfintro')
    corpintro = request.POST.get('corpintro')
    teamintro = request.POST.get('teamintro')
    country = request.POST.get('country')
    prov = request.POST.get('prov')
    group = request.POST.get('group')
    city = request.POST.get('city')
    county = request.POST.get('county')
    try:
        agt = agent_info.objects.get(userid=userid)
    except agent_info.DoesNotExist:
        return HttpResponse(get_res_info('1', 'The user account is invalid!'))
    if fname != None:
        agt.fname = fname
    if lname != None:
        agt.lname = lname
    if tel != None:
        agt.tel = tel
    if email != None:
        agt.email = email
    if address != None:
        agt.address = address
    if corp != None:
        agt.corp = corp
    if note != None:
        agt.note = note
    if website != None:
        agt.website = website
    if postid != None:
        agt.postid = postid
    if username2 != None:
        agt.username2 = username2
    if tel2 != None:
        agt.tel2 = tel2
    if email2 != None:
        agt.email2 = email2
    if selfintro != None:
        agt.selfintro = selfintro
    if corpintro != None:
        agt.corpintro = corpintro
    if teamintro != None:
        agt.teamintro = teamintro
    if country != None:
        agt.country = country
    if prov != None:
        agt.prov = prov
    if group != None:
        agt.group = group
    if city != None:
        agt.city = city
    if county != None:
        agt.county = county
    agt.save()
    if lname != None or fname != None:
        agt.username = agt.fname + ' ' + agt.lname
        agt.save()
    return HttpResponse(get_res_info())


def small_agent_img(target_width, filename):
    # 生成源文件和压缩文件的绝对路径
    os.chdir('/root/myweb/data/')
    filename = os.path.abspath(filename)
    basename = os.path.basename(filename)
    smallname = os.path.join(os.path.dirname(os.path.dirname(filename)),
                             'agentimgs_small', basename)

    if os.path.exists(smallname):
        # 已压缩过的图片
        print '%s already smalled!' % filename
    else:
        im = Image.open(filename)

        # 判断图片的宽和高，以最小的一边为压缩目标，这样不会丢失图片内容
        minside = im.size[0] if im.size[0] <= im.size[1] else im.size[1]
        if minside < target_width:
            im.save(smallname)
        else:

            # 宽高比
            k = im.size[0] * 1.000 / im.size[1]

            # 当宽小于高时，将宽度压缩到目标像素
            if im.size[0] <= im.size[1]:
                n = im.resize((target_width, int(target_width / k)),
                              Image.ANTIALIAS)
            # 当高小于宽时，将高度压缩到目标像素
            else:
                n = im.resize((int(target_width * k), target_width),
                              Image.ANTIALIAS)

            n.save(smallname)
            print '%s smalled!' % filename


def small_agent(request):
    userid = request.GET.get('userid')
    try:
        agt = agent_info.objects.get(userid=userid)
    except agent_info.DoesNotExist:
        return HttpResponse(get_res_info('1', 'The user account is invalid!'))

    if hasattr(agt.head, 'url'):
        small_agent_img(200, agt.head.name)
    if hasattr(agt.qrcode, 'url'):
        small_agent_img(200, agt.qrcode.name)
    if hasattr(agt.logo, 'url'):
        small_agent_img(200, agt.logo.name)
    if hasattr(agt.head2, 'url'):
        small_agent_img(200, agt.head2.name)
    if hasattr(agt.qrcode2, 'url'):
        small_agent_img(200, agt.qrcode2.name)
    if hasattr(agt.qrcode2, 'url'):
        small_agent_img(200, agt.qrcode2.name)
    aimg = agent_img.objects.filter(userid=userid, imgtype='agent')
    for img in aimg:
        small_agent_img(420, img.img.name)

    return HttpResponse(get_res_info())


def upload_img(request):
    print request.FILES
    userid = request.POST.get('userid')
    try:
        agt = agent_info.objects.get(userid=userid)
    except agent_info.DoesNotExist:
        return HttpResponse(get_res_info('1', 'The user account is invalid!'))
    head = request.FILES.get('head')
    qrcode = request.FILES.get('qrcode')
    logo = request.FILES.get('logo')
    head2 = request.FILES.get('head2')
    qrcode2 = request.FILES.get('qrcode2')
    agent = request.FILES.get('agent')
    if head:
        agt.head = head
        agt.save()
        small_agent_img(200, agt.head.name)
        return HttpResponse('head')
    if qrcode:
        agt.qrcode = qrcode
        agt.save()
        small_agent_img(200, agt.qrcode.name)
        return HttpResponse('qrcode')
    if logo:
        agt.logo = logo
        agt.save()
        small_agent_img(200, agt.logo.name)
        return HttpResponse('logo')
    if head2:
        agt.head2 = head2
        agt.save()
        small_agent_img(200, agt.head2.name)
        return HttpResponse('head2')
    if qrcode2:
        agt.qrcode2 = qrcode2
        agt.save()
        small_agent_img(200, agt.qrcode2.name)
        return HttpResponse('qrcode2')
    if agent:
        aimg = agent_img(userid=userid, imgtype='agent', img=agent)
        aimg.save()
        small_agent_img(420, aimg.img.name)
        return HttpResponse(aimg.id)
    return HttpResponse(get_res_info('1', '未接收到图片，请验证图片的key!'))


def del_img(request):
    userid = request.POST.get('userid')
    imgid = request.POST.get('imgid')
    try:
        agt = agent_info.objects.get(userid=userid)
    except agent_info.DoesNotExist:
        return HttpResponse(get_res_info('1', '无效用户名!'))
    if imgid == 'head':
        agt.head = 'agentimgs/def_head.png'
        agt.save()
        return HttpResponse(get_res_info())
    if imgid == 'qrcode':
        agt.qrcode = 'agentimgs/def_qrcode.png'
        agt.save()
        return HttpResponse(get_res_info())
    if imgid == 'logo':
        agt.logo = 'agentimgs/def_logo.png'
        agt.save()
        return HttpResponse(get_res_info())
    if imgid == 'head2':
        agt.head2 = 'agentimgs/def_head.png'
        agt.save()
        return HttpResponse(get_res_info())
    if imgid == 'qrcode2':
        agt.qrcode2 = 'agentimgs/def_qrcode.png'
        agt.save()
        return HttpResponse(get_res_info())
    if imgid != None:
        aimg = agent_img.objects.get(userid=userid, id=imgid)
        aimg.delete()
        return HttpResponse(get_res_info())
    return HttpResponse(get_res_info('1', 'imgid参数错误!'))


def add_card(request):
    userid = request.POST.get('userid')
    holder = request.POST.get('holder')
    cardno = request.POST.get('cardno')
    expire = request.POST.get('expire')
    cvs = request.POST.get('cvs')
    postid = request.POST.get('postid')

    try:
        oldcard = agent_card.objects.get(userid=userid, cardtype='1')
        oldcard.cardtype = '0'
        oldcard.save()
    except agent_card.DoesNotExist:
        pass

    card = agent_card(userid=userid, holder=holder, cardno=cardno,
                      expire=expire, cvs=cvs, postid=postid, cardtype='1')
    card.save()
    return HttpResponse(card.id)


def del_card(request):
    userid = request.POST.get('userid')
    cardid = request.POST.get('cardid')
    try:
        card = agent_card.objects.get(userid=userid, id=cardid)
        card.cardtype = 'deleted'
        card.save()
        return HttpResponse(get_res_info())
    except agent_card.DoesNotExist:
        return HttpResponse(get_res_info('1', '信用卡不存在!'))


def default_card(request):
    userid = request.POST.get('userid')
    cardid = request.POST.get('cardid')
    try:
        card = agent_card.objects.get(userid=userid, id=cardid)
        card.cardtype = '1'
        card.save()
        return HttpResponse(get_res_info())
    except agent_card.DoesNotExist:
        return HttpResponse(get_res_info('1', '信用卡不存在!'))


def get_passwd_code(request):
    userid = request.POST.get('userid')
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    tk = tmp_token(userid=userid, token=code)
    tk.save()
    send_password_code(userid, code)
    return HttpResponse(code)


def update_passwd(request):
    userid = request.POST.get('userid')
    passwd1 = request.POST.get('passwd1')
    passwd2 = request.POST.get('passwd2')
    if passwd1 != passwd2:
        return HttpResponse(get_res_info('1', '密码不一致!'))

    try:
        u = User.objects.get(username=userid)
        u.set_password(passwd1)
        u.save()
        logout(request)
        return HttpResponse(get_res_info())
    except User.DoesNotExist:
        return HttpResponse(get_res_info('2', '用户名不存在!'))


def leave_message(request):
    userid = request.POST.get('userid', '')
    custname = request.POST.get('custname', '')
    custemail = request.POST.get('custemail', '')
    custmsg = request.POST.get('custmsg', '')
    url = request.POST.get('url', '')

    custmsg += '\n%s' % url
    if '/agent3/' in url:
        mail_api('D', userid, custemail, custname, custmsg)
    else:
        mail_api('C', userid, custemail, custname, custmsg)


    msg = cust_message(userid=userid, custname=custname, custemail=custemail,
                       custmsg=custmsg)
    msg.save()
    if userid == '15361990@qq.com':
        someone_subscribe()
    else:
        someone_leave_msg(userid)
    return HttpResponse(get_res_info())


def update_opendate(request):
    #     userid = request.GET.get('userid')
    mls = request.POST.get('mls')
    idx = request.POST.get('idx')
    bgndate = None
    enddate = None
    if request.POST.get('bgndate'):
        bgndate = datetime.datetime.strptime(request.POST.get('bgndate'),
                                             "%Y%m%d%H%M%S")
    if request.POST.get('enddate'):
        enddate = datetime.datetime.strptime(request.POST.get('enddate'),
                                             "%Y%m%d%H%M%S")

    try:
        opendt = Openhouse.objects.get(listingid=mls)
        if idx == '1':
            opendt.bgndate1 = bgndate
            opendt.enddate1 = enddate
        elif idx == '2':
            opendt.bgndate2 = bgndate
            opendt.enddate2 = enddate
        opendt.save()
    except Openhouse.DoesNotExist:
        if idx == '1':
            Openhouse(listingid=mls, bgndate1=bgndate, enddate1=enddate).save()
        elif idx == '2':
            Openhouse(listingid=mls, bgndate2=bgndate, enddate2=enddate).save()

    return HttpResponse(get_res_info())


def get_singlepages(request):
    userid = request.GET.get('userid')
    page = request.GET.get('page')
    tks = Tokens.objects.filter(userid=userid)
    ls = Listing_for_sp.objects.filter(
        token__in=[t.token for t in tks]).order_by('-datadate')
    res = []
    for l in ls:
        tmp = {}
        tmp['mls'] = l.listingid
        tmp['price'] = l.price
        tmp['salestatus'] = l.salestatus
        tmp['url'] = l.url
        tmp[
            'consoleurl'] = 'http://www.realtoraccess.com/sp/bi/?mls=%s&token=%s' % (
            l.listingid, l.token)
        tmp['visit'] = l.visit
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['opendate1'] = '-'
        tmp['opendate2'] = '-'
        tmp['address'] = l.listingname
        tmp['token'] = l.token
        tmp['sptype'] = l.sptype
        try:
            opendt = Openhouse.objects.get(listingid=l.listingid)
            tmp['opendate1'] = (opendt.bgndate1.strftime(
                '%Y%m%d%H%M%S') if opendt.bgndate1 != None else '') + '-' + \
                               (opendt.enddate1.strftime(
                                   '%Y%m%d%H%M%S') if opendt.enddate1 != None else '')
            tmp['opendate2'] = (opendt.bgndate2.strftime(
                '%Y%m%d%H%M%S') if opendt.bgndate2 != None else '') + '-' + \
                               (opendt.enddate2.strftime(
                                   '%Y%m%d%H%M%S') if opendt.enddate2 != None else '')
        except Openhouse.DoesNotExist:
            pass
        res.append(tmp)
    return HttpResponse(json.dumps(res, indent=2, ensure_ascii=False))


def set_sale_status(request):
    token = request.POST.get('token')
    salestatus = request.POST.get('salestatus')
    ls = Listing_for_sp.objects.get(token=token)
    ls.salestatus = salestatus
    ls.save()
    return HttpResponse('ok')


def askfor_invoice(request):
    orderid = request.GET.get('orderid')
    userid = request.GET.get('userid')
    aa = agent_auth.objects.get(id=orderid)

    service = {}
    service['vip'] = 'Hosting'
    service['auth'] = 'Translationg & Verification'
    service['sp'] = 'Smartflyer'
    service['domain'] = 'Domain'

    ivc = {}
    ivc['fee'] = aa.fee
    ivc['service'] = service.get(aa.service)
    ivc['token'] = aa.token

    ask_for_voince(userid, ivc)
    return HttpResponse('ok')


def login_page(request):
    return render_to_response('web/login.html')


def signup_page(request):
    return render_to_response('web/register.html')


def agent2_page(request, uid):
    user = agent_info.objects.get(id=uid)
    if user.userid == 'amir@amirmiri.com':
        return redirect('/')
    if not agent_auth.objects.filter(userid=user.userid, status='paid',
                                     service='vip'):
        return redirect('/web/agent/%s' % user.id, permanent=True)

    if agent_auth.objects.filter(userid=user.userid, status='paid',
                                 service='auth'):
        auth = 1
    else:
        auth = 0

    visit = Access_hitory.objects.filter(htmltype='agenthome',
                                         userid=user.userid).count()

    if user.userid == 'Alfie@alfieyang.com':
        tks = Tokens.objects.filter(
            userid__in=['Alfie@alfieyang.com', 'zachtchester@gmail.com'])
    else:
        tks = Tokens.objects.filter(userid=user.userid)
    ls = Listing_for_sp.objects.filter(token__in=[t.token for t in tks],
                                       ).order_by('-datadate')
    lsts = []
    for l in ls:
        if l.salestatus == 'invalid':
            continue
        tmp = {}
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)

    # 按经纪所属城市，推荐房源占位
    if len(lsts) < 4:
        if user.city != '':
            sql = "SELECT srcdata FROM app.`t99_cityname`WHERE cityid = '%s'" % user.city
            usercity = ''
            for row in MySql.sel_table(sql):
                usercity = row[0]
            ls1 = Listing.objects.raw("""
                            SELECT a.* FROM app.`app_listing` a
                            WHERE cityname = '%s'
                            ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                        """ % usercity)
        else:
            ls1 = Listing.objects.filter(
                listingid__in=('r2265452', 'r2263196', 'r2263429', 'r2261163'))
        for l in ls1:
            tmp = {}
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    imgs = []
    vdo = ''
    for i in agent_img.objects.filter(userid=user.userid):
        if i.imgtype == 'agent':
            imgs.append({'img': i.img.url, 'imgid': i.id})
        elif i.imgtype == 'video':
            vdo = i.img.url

    if len(imgs) == 0:
        imgs.append({
            'img': 'http://www.realtoraccess.com/static/web/img/def_selfimg.png',
            'imgid': 999})

    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)

    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='agenthome',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    usercity = get_cityname(user.city)
    res = render_to_response('web/agent.html',
                             {'user': user, 'usercity': usercity,
                              'visit': visit, 'auth': auth, 'ls': lsts,
                              'imgs': imgs, 'atc': atcs, 'vdo': vdo})
    res['X-Frame-Options'] = 'ALLOWALL'
    return res


def place_holder():
    tokens = Tokens.objects.filter(userid='diao.xc@qq.com')
    tks = [tk.token for tk in tokens]
    listings = Listing_for_sp.objects.filter(token__in=tks).order_by('-datadate')
    return listings


def agent3_page(request, uid):
    user = agent_info.objects.get(id=uid)
    if user.userid in ('amir@amirmiri.com', 'juliewang321@hotmail.com'):
        return redirect('/')
    # if agent_auth.objects.filter(userid=user.userid, status='paid',
    #                              service='diyPage'):
    #     return redirect('/web/agent4/%s' % user.id, permanent=True)

    if agent_auth.objects.filter(userid=user.userid, status='paid',
                                 service='auth'):
        auth = 1
    else:
        auth = 0
    vdo = ''
    visit = Access_hitory.objects.filter(htmltype='agenthome',
                                         userid=user.userid).count()
    tks = Tokens.objects.filter(userid=user.userid)
    tokens = [t.token for t in tks]
    ls = Listing_for_sp.objects.filter(token__in=tokens).order_by('-datadate')
    lsts = []
    lsts2 = []
    for l in ls:
        if l.salestatus == 'invalid':
            continue
        tmp = {}
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['token'] = l.token
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        if l.salestatus not in ('yes', 'invalid'):
            lsts.append(tmp)
        elif l.salestatus == 'yes':
            for i in Listingimg.objects.filter(listingid=l.listingid):
                if 'from_addlisting.jpg' in i.imgname:
                    tmp['img'] = i.img.url
                    break
            lsts2.append(tmp)

    # 按经纪所属城市，推荐房源占位
    if len(lsts) < 4:
        if user.city != '':
            sql = "SELECT srcdata FROM app.`t99_cityname`WHERE cityid = '%s'" % user.city
            usercity = ''
            for row in MySql.sel_table(sql):
                usercity = row[0]
            ls1 = Listing_for_sp.objects.filter(distid=usercity).order_by('-datadate')
            if len(ls1) == 0:
                ls1 = place_holder()

        else:
            ls1 = Listing.objects.filter(
                listingid__in=('r2265452', 'r2263196', 'r2263429', 'r2261163'))
        for l in ls1:
            tmp = {}
            tmp['mls'] = l.listingid
            tmp['url'] = l.url
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    if len(lsts2) < 4:
        ls2 = Listing_for_sp.objects.filter(salestatus='no').order_by('datadate')
        for l in ls2:
            if l.token in tokens or l.sptype == 'custom' or l.salestatus == 'invalid' or l.isspread == '0':
                continue
            tmp = {}
            tmp['mls'] = l.listingid
            tmp['url'] = l.url
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
                l.distid)
            tmp['salestatus'] = l.salestatus
            tmp['sptype'] = 'smf'
            tmp['token'] = l.token
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts2.append(tmp)
            if len(lsts2) == 4:
                break

    imgs = []

    for i in agent_img.objects.filter(userid=user.userid):
        if i.imgtype == 'agent':
            imgs.append({'img': i.img.url, 'imgid': i.id})
        if i.imgtype == 'video':
            vdo = i.img.url
    if len(imgs) == 0:
        imgs.append({
            'img': 'http://www.realtoraccess.com/static/web/img/def_selfimg.png',
            'imgid': 999})
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)

    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='agenthome',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    usercity = get_cityname(user.city)
    res = render_to_response('web/agent2.html',
                             {'user': user, 'usercity': usercity,
                              'visit': visit, 'auth': auth, 'ls': lsts,
                              'ls2': lsts2, 'imgs': imgs, 'atc': atcs, 'vdo': vdo})
    res['X-Frame-Options'] = 'ALLOWALL'
    return res

def agent4_page(request,uid):
    ui = agent_info.objects.get(id=uid)
    if ui.userid in ('amir@amirmiri.com', 'juliewang321@hotmail.com'):
        return redirect('/')
    # if not agent_auth.objects.filter(userid=ui.userid, status='paid',
    #                                  service='diyPage'):
    #     return redirect('/web/agent3/%s' % ui.id, permanent=True)
    return render_to_response('web/agent4/template/index.html', {'user': ui})

def update_visit(request):
    token = request.POST.get('token')
    l = Listing_for_sp.objects.get(token=token)
    l.visit += 1
    l.save()
    return HttpResponse('ok')


def add_email(request):
    userid = request.POST.get('userid')
    useremail = request.POST.get('useremail').strip()
    try:
        MessageCenter.objects.get(agentid=userid, user_email=useremail,
                                  msg_type='agent_page_3')
    except MessageCenter.DoesNotExist:
        MessageCenter.objects.create(agentid=userid, user_email=useremail,
                                     msg_type='agent_page_3',
                                     user_ip=request.META.get('REMOTE_ADDR'))
    return HttpResponse('ok')


@login_required(login_url='/web/page/signin/')
def agent_console_page(request):
    # userinfo
    try:
        userobj = agent_info.objects.get(userid=request.user)
    except agent_info.DoesNotExist:
        return redirect('/web/page/signin')
    user = json.dumps(model_to_dict(userobj), indent=2, ensure_ascii=False,
                      cls=MyEncoder)

    # cardinfo
    try:
        card = agent_card.objects.get(userid=userobj.userid, cardtype='1')
        card = json.dumps(model_to_dict(card), indent=2, ensure_ascii=False,
                          cls=MyEncoder)
    except agent_card.DoesNotExist:
        card = {}

    # orderinfo
    od = agent_auth.objects.filter(userid=userobj.userid).order_by('-bgndate')
    tmp = {}
    engagement = 'false'
    subscript = 'false'
    for o in od:
        if o.service == 'engagement' and o.status == 'paid':
            engagement = 'true'
        if o.service == 'subscription' and o.status == 'paid':
            subscript = 'true'
        if not tmp.get(o.cardno):
            tmp[o.cardno] = []
        tmp[o.cardno].append(
            {'orderid': str(o.id), 'fee': str(o.fee), 'status': str(o.status),
             'date': o.bgndate.strftime('%Y-%m-%d') if o.bgndate is not None else '',
             'invoice': 'www.realtoraccess.com/get-invoice/'})
    orders = []
    for t in tmp:
        orders.append({'cardno': str(t), 'records': tmp.get(t)})

    # agent imgs
    ai = agent_img.objects.filter(userid=userobj.userid, imgtype='agent')
    imgs = []
    for i in ai:
        imgs.append({'imgid': str(i.id), 'img': i.img.url})

    emailhistory = [{
        'date': 'Tuesday 6:00 AM',
        'emaildelivery': 'You have no list yet!',
        'reviewemail': 'http://www.realtoraccess.com/news/3443'
    }]
    return render_to_response('web/console.html',
                              {'user': user, 'card': card, 'orders': orders,
                               'imgs': imgs, 'emailhistory': emailhistory
                                  , 'engagement': engagement, 'subscript':subscript})


def upload_email_list(request):
    userid = request.POST.get('userid')
    excel = request.FILES.get('file')
    exl = agent_img(userid=userid, imgtype='emaillist', img=excel)
    exl.save()
    for row in get_content(r"/root/myweb/data/" + exl.img.name, 'Sheet1',
                           skiprow=1, skipcol=0):
        try:
            MessageCenter.objects.get(agentid=userid, user_email=row[2].strip(),
                                      msg_type='excel_upload')
        except MessageCenter.DoesNotExist:
            MessageCenter.objects.create(agentid=userid,
                                         user_name=row[0] + ' ' + row[1],
                                         user_email=row[2].strip(),
                                         msg_type='excel_upload',
                                         src_url=exl.img.name,
                                         user_ip=request.META.get('REMOTE_ADDR'))
    return HttpResponse('1')


def set_schedule(request):
    userid = request.POST.get('userid')
    scd = request.POST.get('schedule')
    agt = agent_info.objects.get(userid=userid)
    agt.emailscd = scd
    agt.save()
    return HttpResponse('1')


def set_price(request):
    token = request.POST.get('token')
    price = request.POST.get('price')
    try:
        l = Listing_for_sp.objects.get(token=token)
        l.price = price
        l.save()
    except Listing_for_sp.DoesNotExist:
        pass
    return HttpResponse('1')


def add_listing(request):
    userid = request.POST.get('userid')
    mls = request.POST.get('mls')
    address = request.POST.get('address')
    if mls == '':
        mls = address.replace(' ', '')
    price = request.POST.get('price')
    sqft = request.POST.get('sqft')
    housetype = request.POST.get('housetype')
    area = request.POST.get('area')
    url = request.POST.get('url')
    img = request.FILES.get('file')
    dist = request.POST.get('dist','')
    token = uuid.uuid1()
    Tokens(token=token, tokentype='user', active='1', userid=userid).save()
    sp = Listing_for_sp(listingid=mls, listingname=address, price=price,
                        areas=sqft, housetype=housetype, cityname=area,
                        token=token, url=url, sptype='custom',distid=dist,
                        isspread='1')
    sp.save()
    limg = Listingimg(listingid=mls, img=img,
                      imgname='%s_from_addlisting.jpg' % mls,
                      imgtype='listing1')
    limg.save()

    target_width = 400
    #     os.chdir(r'E:\Job\workspace\reator\data')
    os.chdir('/root/myweb/data/')
    filename = limg.img.name
    filename = os.path.abspath(filename)
    basename = os.path.basename(filename)
    smallname = os.path.join(os.path.dirname(os.path.dirname(filename)),
                             'listings_small', basename)

    im = Image.open(filename)
    # 判断图片的宽和高，以最小的一边为压缩目标，这样不会丢失图片内容
    minside = im.size[0] if im.size[0] <= im.size[1] else im.size[1]
    if minside < target_width:
        im.save(smallname)
    else:
        k = im.size[0] * 1.000 / im.size[1]

        # 当宽小于高时，将宽度压缩到目标像素
        if im.size[0] <= im.size[1]:
            n = im.resize((target_width, int(target_width / k)),
                          Image.ANTIALIAS)
        # 当高小于宽时，将高度压缩到目标像素
        else:
            n = im.resize((int(target_width * k), target_width),
                          Image.ANTIALIAS)

        n.save(smallname)
        print '%s smalled!' % filename

    res = {}
    res['mls'] = sp.listingid
    res['price'] = sp.price
    res['salestatus'] = sp.salestatus
    res['url'] = sp.url
    res['consoleurl'] = 'http://www.webmainland.com/sp/bi/?mls=%s&token=%s' % (
        sp.listingid, sp.token)
    res['visit'] = sp.visit
    res['date'] = sp.datadate.strftime('%Y-%m-%d')
    res['opendate1'] = '-'
    res['opendate2'] = '-'
    res['address'] = sp.listingname
    res['token'] = str(sp.token)
    res['sptype'] = sp.sptype

    return HttpResponse(json.dumps(res, indent=2, ensure_ascii=False))


def realtyninja_page(request):
    return render_to_response('web/realtyninja.html')


def passwd_page(request):
    return render_to_response('web/password.html')


def console_page_redirect(request):
    return redirect('/web/console/', permanent=True)


def login_page_redirect(request):
    return redirect('/web/page/signin/', permanent=True)


def signup_page_redirect(request):
    frm = request.GET.get('from')
    print frm
    print 'aaaaaaaaaaaaaaaa'
    if frm:
        r = '/web/page/signup/?from=' + frm
    else:
        r = '/web/page/signup/'
    return redirect(r, permanent=True)


def bi_page_vancouver(request):
    user = agent_info.objects.get(userid="yaletownrealtor@gmail.com")
    usercity = get_cityname(user.city)
    sql = """
            SELECT cityid,cityname,format(AVG(price_avg),0),MAX(price_avg),MIN(price_avg)
            FROM app.`ana_listing_price`
            WHERE cityid IN ('Vancouver','WestVan','Burnaby','Surrey','Coquitlam','WhiteRock','PortMoody','Richmond','NorthVancouver','NorthSurrey','NewWestminster','Whistler')
            GROUP BY cityid,cityname
            """
    prices = {}
    for row in MySql.sel_table(sql):
        prices[row[0]] = {'cityname': row[1], 'price': row[2],
                          'maxprice': row[3], 'minprice': row[4]}

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='VancouverWest',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype

        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_countyname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)
    if len(lsts) < 4:
        ls1 = Listing.objects.raw("""
                        SELECT a.* FROM app.`app_listing` a
                        WHERE cityname = 'VancouverWest'
                        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                    """)
        for l in ls1:
            tmp = {}
            u = agent_info.objects.get(userid='diao.xc@qq.com')
            tmp['head'] = u.head.url
            tmp['usercity'] = get_cityname(u.city)
            tmp['username'] = u.username
            tmp['uid'] = u.id
            tmp['ltype'] = '特色房源'
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='VancouverEast',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts2 = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype

        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_countyname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts2.append(tmp)

    # 文章
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)

    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='bi_van',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    visit = Access_hitory.objects.filter(htmltype='bi_van').count()
    return render_to_response('web/ana_van.html',
                              {'user': user, 'usercity': usercity,
                               'prices': prices, 'atc': atcs, 'ls': lsts,
                               'ls2': lsts2, 'visit': visit + 2834})


def bi_page_westvan(request):
    user = agent_info.objects.get(userid="michellevaughan@shaw.ca")
    usercity = get_cityname(user.city)
    sql = """
            SELECT cityid,cityname,format(AVG(price_avg),0),MAX(price_avg),MIN(price_avg)
            FROM app.`ana_listing_price`
            WHERE cityid IN ('Vancouver','WestVan','Burnaby','Surrey','Coquitlam','WhiteRock','PortMoody','Richmond','NorthVancouver','NorthSurrey','NewWestminster','Whistler')
            GROUP BY cityid,cityname
            """
    prices = {}
    for row in MySql.sel_table(sql):
        prices[row[0]] = {'cityname': row[1], 'price': row[2],
                          'maxprice': row[3], 'minprice': row[4]}

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='WestVan',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype

        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)
    if len(lsts) < 4:
        ls1 = Listing.objects.raw("""
                        SELECT a.* FROM app.`app_listing` a
                        WHERE cityname = 'WestVan'
                        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                    """)
        for l in ls1:
            tmp = {}
            u = agent_info.objects.get(userid='diao.xc@qq.com')
            tmp['head'] = u.head.url
            tmp['usercity'] = get_cityname(u.city)
            tmp['username'] = u.username
            tmp['uid'] = u.id
            tmp['ltype'] = '特色房源'
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    # 文章
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='bi_westvan',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    visit = Access_hitory.objects.filter(htmltype='bi_westvan').count()
    return render_to_response('web/ana_westvan.html',
                              {'user': user, 'usercity': usercity,
                               'prices': prices, 'atc': atcs, 'ls': lsts,
                               'visit': visit + 2212})


def bi_page_burnaby(request):
    user = agent_info.objects.get(userid="mwtsang@aol.com")
    usercity = get_cityname(user.city)
    sql = """
            SELECT cityid,cityname,format(AVG(price_avg),0),MAX(price_avg),MIN(price_avg)
            FROM app.`ana_listing_price`
            WHERE cityid IN ('Vancouver','WestVan','Burnaby','Surrey','Coquitlam','WhiteRock','PortMoody','Richmond','NorthVancouver','NorthSurrey','NewWestminster','Whistler')
            GROUP BY cityid,cityname
            """
    prices = {}
    for row in MySql.sel_table(sql):
        prices[row[0]] = {'cityname': row[1], 'price': row[2],
                          'maxprice': row[3], 'minprice': row[4]}

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='Burnaby',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)
    if len(lsts) < 4:
        ls1 = Listing.objects.raw("""
                        SELECT a.* FROM app.`app_listing` a
                        WHERE cityname = 'Burnaby'
                        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                    """)
        for l in ls1:
            tmp = {}
            u = agent_info.objects.get(userid='diao.xc@qq.com')
            tmp['head'] = u.head.url
            tmp['usercity'] = get_cityname(u.city)
            tmp['username'] = u.username
            tmp['uid'] = u.id
            tmp['ltype'] = '特色房源'
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    # 文章
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)

    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='bi_burnaby',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    visit = Access_hitory.objects.filter(htmltype='bi_burnaby').count()
    return render_to_response('web/ana_burnaby.html',
                              {'user': user, 'usercity': usercity,
                               'prices': prices, 'atc': atcs, 'ls': lsts,
                               'visit': visit + 1232})


def bi_page_surrey(request):
    user = agent_info.objects.get(userid="chris@chrisdavidson.ca")
    usercity = get_cityname(user.city)
    sql = """
            SELECT cityid,cityname,format(AVG(price_avg),0),MAX(price_avg),MIN(price_avg)
            FROM app.`ana_listing_price`
            WHERE cityid IN ('Vancouver','WestVan','Burnaby','Surrey','Coquitlam','WhiteRock','PortMoody','Richmond','NorthVancouver','NorthSurrey','NewWestminster','Whistler')
            GROUP BY cityid,cityname
            """
    prices = {}
    for row in MySql.sel_table(sql):
        prices[row[0]] = {'cityname': row[1], 'price': row[2],
                          'maxprice': row[3], 'minprice': row[4]}

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='Surrey',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_countyname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)
    if len(lsts) < 4:
        ls1 = Listing.objects.raw("""
                        SELECT a.* FROM app.`app_listing` a
                        WHERE cityname = 'Surrey'
                        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                    """)
        for l in ls1:
            tmp = {}
            u = agent_info.objects.get(userid='diao.xc@qq.com')
            tmp['head'] = u.head.url
            tmp['usercity'] = get_cityname(u.city)
            tmp['username'] = u.username
            tmp['uid'] = u.id
            tmp['ltype'] = '特色房源'
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='Cloverdale',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts2 = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_countyname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)
    if len(lsts2) < 4:
        ls1 = Listing.objects.raw("""
                        SELECT a.* FROM app.`app_listing` a
                        WHERE cityname = 'Cloverdale'
                        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                    """)
        for l in ls1:
            tmp = {}
            u = agent_info.objects.get(userid='diao.xc@qq.com')
            tmp['head'] = u.head.url
            tmp['usercity'] = get_cityname(u.city)
            tmp['username'] = u.username
            tmp['uid'] = u.id
            tmp['ltype'] = '特色房源'
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts2.append(tmp)
            if len(lsts2) == 4:
                break

    # 文章
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='bi_surrey',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    visit = Access_hitory.objects.filter(htmltype='bi_surrey').count()
    return render_to_response('web/ana_surrey.html',
                              {'user': user, 'usercity': usercity,
                               'prices': prices, 'atc': atcs, 'ls': lsts,
                               'ls2': lsts2, 'visit': visit + 2124})


def bi_page_coquitlam(request):
    user = agent_info.objects.get(userid="zachtchester@gmail.com")
    usercity = get_cityname(user.city)
    sql = """
            SELECT cityid,cityname,format(AVG(price_avg),0),MAX(price_avg),MIN(price_avg)
            FROM app.`ana_listing_price`
            WHERE cityid IN ('Vancouver','WestVan','Burnaby','Surrey','Coquitlam','WhiteRock','PortMoody','Richmond','NorthVancouver','NorthSurrey','NewWestminster','Whistler')
            GROUP BY cityid,cityname
            """
    prices = {}
    for row in MySql.sel_table(sql):
        prices[row[0]] = {'cityname': row[1], 'price': row[2],
                          'maxprice': row[3], 'minprice': row[4]}

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='Coquitlam',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)
    if len(lsts) < 4:
        ls1 = Listing.objects.raw("""
                        SELECT a.* FROM app.`app_listing` a
                        WHERE cityname = 'Coquitlam'
                        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                    """)
        for l in ls1:
            tmp = {}
            u = agent_info.objects.get(userid='diao.xc@qq.com')
            tmp['head'] = u.head.url
            tmp['usercity'] = get_cityname(u.city)
            tmp['username'] = u.username
            tmp['uid'] = u.id
            tmp['ltype'] = '特色房源'
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    # 文章
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='bi_coquitlam',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    visit = Access_hitory.objects.filter(htmltype='bi_coquitlam').count()
    return render_to_response('web/ana_coquitlam.html',
                              {'user': user, 'usercity': usercity,
                               'prices': prices, 'atc': atcs, 'ls': lsts,
                               'visit': visit + 1297})


def bi_page_whiterock(request):
    user = agent_info.objects.get(userid="E.dave@davesnider.ca")
    usercity = get_cityname(user.city)
    sql = """
            SELECT cityid,cityname,format(AVG(price_avg),0),MAX(price_avg),MIN(price_avg)
            FROM app.`ana_listing_price`
            WHERE cityid IN ('Vancouver','WestVan','Burnaby','Surrey','Coquitlam','WhiteRock','PortMoody','Richmond','NorthVancouver','NorthSurrey','NewWestminster','Whistler')
            GROUP BY cityid,cityname
            """
    prices = {}
    for row in MySql.sel_table(sql):
        prices[row[0]] = {'cityname': row[1], 'price': row[2],
                          'maxprice': row[3], 'minprice': row[4]}

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='WhiteRock',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)
    if len(lsts) < 4:
        ls1 = Listing.objects.raw("""
                        SELECT a.* FROM app.`app_listing` a
                        WHERE cityname = 'WhiteRock'
                        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                    """)
        for l in ls1:
            tmp = {}
            u = agent_info.objects.get(userid='diao.xc@qq.com')
            tmp['head'] = u.head.url
            tmp['usercity'] = get_cityname(u.city)
            tmp['username'] = u.username
            tmp['uid'] = u.id
            tmp['ltype'] = '特色房源'
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    # 文章
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='bi_whiterock',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    visit = Access_hitory.objects.filter(htmltype='bi_whiterock').count()
    return render_to_response('web/ana_whiterock.html',
                              {'user': user, 'usercity': usercity,
                               'prices': prices, 'atc': atcs, 'ls': lsts,
                               'visit': visit + 1239})


def bi_page_portmoody(request):
    user = agent_info.objects.get(userid="colin@colindavidson.ca")
    usercity = get_cityname(user.city)
    sql = """
            SELECT cityid,cityname,format(AVG(price_avg),0),MAX(price_avg),MIN(price_avg)
            FROM app.`ana_listing_price`
            WHERE cityid IN ('Vancouver','WestVan','Burnaby','Surrey','Coquitlam','WhiteRock','PortMoody','Richmond','NorthVancouver','NorthSurrey','NewWestminster','Whistler')
            GROUP BY cityid,cityname
            """
    prices = {}
    for row in MySql.sel_table(sql):
        prices[row[0]] = {'cityname': row[1], 'price': row[2],
                          'maxprice': row[3], 'minprice': row[4]}

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='PortMoody',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)
    if len(lsts) < 4:
        ls1 = Listing.objects.raw("""
                        SELECT a.* FROM app.`app_listing` a
                        WHERE cityname = 'PortMoody'
                        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                    """)
        for l in ls1:
            tmp = {}
            u = agent_info.objects.get(userid='diao.xc@qq.com')
            tmp['head'] = u.head.url
            tmp['usercity'] = get_cityname(u.city)
            tmp['username'] = u.username
            tmp['uid'] = u.id
            tmp['ltype'] = '特色房源'
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    # 文章
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='bi_portmoody',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    visit = Access_hitory.objects.filter(htmltype='bi_portmoody').count()
    return render_to_response('web/ana_portmoody.html',
                              {'user': user, 'usercity': usercity,
                               'prices': prices, 'atc': atcs, 'ls': lsts,
                               'visit': visit + 1589})


def bi_page_richmond(request):
    user = agent_info.objects.get(userid="haileycc0127@gmail.com")
    usercity = get_cityname(user.city)
    sql = """
            SELECT cityid,cityname,format(AVG(price_avg),0),MAX(price_avg),MIN(price_avg)
            FROM app.`ana_listing_price`
            WHERE cityid IN ('Vancouver','WestVan','Burnaby','Surrey','Coquitlam','WhiteRock','PortMoody','Richmond','NorthVancouver','NorthSurrey','NewWestminster','Whistler')
            GROUP BY cityid,cityname
            """
    prices = {}
    for row in MySql.sel_table(sql):
        prices[row[0]] = {'cityname': row[1], 'price': row[2],
                          'maxprice': row[3], 'minprice': row[4]}

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='Richmond',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)
    if len(lsts) < 4:
        ls1 = Listing.objects.raw("""
                        SELECT a.* FROM app.`app_listing` a
                        WHERE cityname = 'Richmond'
                        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                    """)
        for l in ls1:
            tmp = {}
            u = agent_info.objects.get(userid='diao.xc@qq.com')
            tmp['head'] = u.head.url
            tmp['usercity'] = get_cityname(u.city)
            tmp['username'] = u.username
            tmp['uid'] = u.id
            tmp['ltype'] = '特色房源'
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    # 文章
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='bi_richmond',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    visit = Access_hitory.objects.filter(htmltype='bi_richmond').count()
    return render_to_response('web/ana_richmond.html',
                              {'user': user, 'usercity': usercity,
                               'prices': prices, 'atc': atcs, 'ls': lsts,
                               'visit': visit + 1267})


def bi_page_northvan(request):
    user = agent_info.objects.get(userid="info@titacool.com")
    usercity = get_cityname(user.city)
    sql = """
            SELECT cityid,cityname,format(AVG(price_avg),0),MAX(price_avg),MIN(price_avg)
            FROM app.`ana_listing_price`
            WHERE cityid IN ('Vancouver','WestVan','Burnaby','Surrey','Coquitlam','WhiteRock','PortMoody','Richmond','NorthVancouver','NorthSurrey','NewWestminster','Whistler')
            GROUP BY cityid,cityname
            """
    prices = {}
    for row in MySql.sel_table(sql):
        prices[row[0]] = {'cityname': row[1], 'price': row[2],
                          'maxprice': row[3], 'minprice': row[4]}

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='NorthVancouver',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)
    if len(lsts) < 4:
        ls1 = Listing.objects.raw("""
                        SELECT a.* FROM app.`app_listing` a
                        WHERE cityname = 'NorthVancouver'
                        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                    """)
        for l in ls1:
            tmp = {}
            u = agent_info.objects.get(userid='diao.xc@qq.com')
            tmp['head'] = u.head.url
            tmp['usercity'] = get_cityname(u.city)
            tmp['username'] = u.username
            tmp['uid'] = u.id
            tmp['ltype'] = '特色房源'
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    # 文章
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='bi_northvan',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    visit = Access_hitory.objects.filter(htmltype='bi_northvan').count()
    return render_to_response('web/ana_northvan.html',
                              {'user': user, 'usercity': usercity,
                               'prices': prices, 'atc': atcs, 'ls': lsts,
                               'visit': visit + 1432})


def bi_page_northsurrey(request):
    user = agent_info.objects.get(userid="mnicolsrealty@gmail.com")
    usercity = get_cityname(user.city)
    sql = """
            SELECT cityid,cityname,format(AVG(price_avg),0),MAX(price_avg),MIN(price_avg)
            FROM app.`ana_listing_price`
            WHERE cityid IN ('Vancouver','WestVan','Burnaby','Surrey','Coquitlam','WhiteRock','PortMoody','Richmond','NorthVancouver','NorthSurrey','NewWestminster','Whistler')
            GROUP BY cityid,cityname
            """
    prices = {}
    for row in MySql.sel_table(sql):
        prices[row[0]] = {'cityname': row[1], 'price': row[2],
                          'maxprice': row[3], 'minprice': row[4]}

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='NorthSurrey',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)
    if len(lsts) < 4:
        ls1 = Listing.objects.raw("""
                        SELECT a.* FROM app.`app_listing` a
                        WHERE cityname = 'NorthSurrey'
                        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                    """)
        for l in ls1:
            tmp = {}
            u = agent_info.objects.get(userid='diao.xc@qq.com')
            tmp['head'] = u.head.url
            tmp['usercity'] = get_cityname(u.city)
            tmp['username'] = u.username
            tmp['uid'] = u.id
            tmp['ltype'] = '特色房源'
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    # 文章
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='bi_northsurrey',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    visit = Access_hitory.objects.filter(htmltype='bi_northsurrey').count()
    return render_to_response('web/ana_northsurrey.html',
                              {'user': user, 'usercity': usercity,
                               'prices': prices, 'atc': atcs, 'ls': lsts,
                               'visit': visit + 2121})


def bi_page_newwestminster(request):
    user = agent_info.objects.get(userid="billwan.re@gmail.com")
    usercity = get_cityname(user.city)
    sql = """
            SELECT cityid,cityname,format(AVG(price_avg),0),MAX(price_avg),MIN(price_avg)
            FROM app.`ana_listing_price`
            WHERE cityid IN ('Vancouver','WestVan','Burnaby','Surrey','Coquitlam','WhiteRock','PortMoody','Richmond','NorthVancouver','NorthSurrey','NewWestminster','Whistler')
            GROUP BY cityid,cityname
            """
    prices = {}
    for row in MySql.sel_table(sql):
        prices[row[0]] = {'cityname': row[1], 'price': row[2],
                          'maxprice': row[3], 'minprice': row[4]}

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='NewWestminster',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)
    if len(lsts) < 4:
        ls1 = Listing.objects.raw("""
                        SELECT a.* FROM app.`app_listing` a
                        WHERE cityname = 'NewWestminster'
                        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                    """)
        for l in ls1:
            tmp = {}
            u = agent_info.objects.get(userid='diao.xc@qq.com')
            tmp['head'] = u.head.url
            tmp['usercity'] = get_cityname(u.city)
            tmp['username'] = u.username
            tmp['uid'] = u.id
            tmp['ltype'] = '特色房源'
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    # 文章
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='bi_newwestminster',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    visit = Access_hitory.objects.filter(htmltype='bi_newwestminster').count()
    return render_to_response('web/ana_newwestminster.html',
                              {'user': user, 'usercity': usercity,
                               'prices': prices, 'atc': atcs, 'ls': lsts,
                               'visit': visit + 1129})


def bi_page_whistler(request):
    user = agent_info.objects.get(userid="brenda@brendarussell.ca")
    usercity = get_cityname(user.city)
    sql = """
            SELECT cityid,cityname,format(AVG(price_avg),0),MAX(price_avg),MIN(price_avg)
            FROM app.`ana_listing_price`
            WHERE cityid IN ('Vancouver','WestVan','Burnaby','Surrey','Coquitlam','WhiteRock','PortMoody','Richmond','NorthVancouver','NorthSurrey','NewWestminster','Whistler')
            GROUP BY cityid,cityname
            """
    prices = {}
    for row in MySql.sel_table(sql):
        prices[row[0]] = {'cityname': row[1], 'price': row[2],
                          'maxprice': row[3], 'minprice': row[4]}

    # 区域房源
    ls = Listing_for_sp.objects.filter(distid='Whistler',
                                       salestatus__in=['no', 'dark'],
                                       isspread='1').order_by('-datadate')
    lsts = []
    for l in ls:
        tmp = {}
        tk = Tokens.objects.get(token=l.token)
        u = agent_info.objects.get(userid=tk.userid)
        tmp['head'] = u.head.url
        tmp['usercity'] = get_cityname(u.city)
        tmp['username'] = u.username
        tmp['uid'] = u.id
        tmp['ltype'] = l.listingtype
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['sptype'] = l.sptype
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        lsts.append(tmp)
    if len(lsts) < 4:
        ls1 = Listing.objects.raw("""
                        SELECT a.* FROM app.`app_listing` a
                        WHERE cityname = 'Whistler'
                        ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
                    """)
        for l in ls1:
            tmp = {}
            u = agent_info.objects.get(userid='diao.xc@qq.com')
            tmp['head'] = u.head.url
            tmp['usercity'] = get_cityname(u.city)
            tmp['username'] = u.username
            tmp['uid'] = u.id
            tmp['ltype'] = '特色房源'
            tmp['mls'] = l.listingid
            tmp['url'] = '/web/listing1/%s/' % l.listingid
            tmp['price'] = l.price
            tmp['address'] = l.listingname
            tmp['areas'] = l.areas
            tmp['housetype'] = get_housetype_name(l.housetype)
            tmp['visit'] = l.visit
            tmp['cityname'] = get_cityname(l.cityname)
            tmp['salestatus'] = 'no'
            tmp['sptype'] = 'smf'
            tmp['date'] = l.datadate.strftime('%Y-%m-%d')
            tmp['img'] = ''
            for i in Listingimg.objects.filter(listingid=l.listingid):
                tmp['img'] = i.img.url
                break
            if tmp['img'] == '':
                continue
            lsts.append(tmp)
            if len(lsts) == 4:
                break

    # 文章
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = {}
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)
    his = Access_hitory(addr=request.META['REMOTE_ADDR'], actiontype='query',
                        htmltype='bi_whistler',
                        agent=request.META['HTTP_USER_AGENT']
                        , referer=request.META.get('HTTP_REFERER', 'url'),
                        userid=user.userid)
    his.save()
    visit = Access_hitory.objects.filter(htmltype='bi_whistler').count()
    return render_to_response('web/ana_whistler.html',
                              {'user': user, 'usercity': usercity,
                               'prices': prices, 'atc': atcs, 'ls': lsts,
                               'visit': visit + 982})


def gen_token(request):
    email = request.GET.get('email')
    tm = get_now()
    tk = Tokens(token=tm, tokentype='user', active='1', userid=email)
    tk.save()
    return HttpResponse('token is %s' % tm)

def get_dist_tree(request):
    sql = 'SELECT cityid FROM app.`t99_cityname` WHERE cityid IS NOT NULL'

    res_data = []
    for row2 in MySql.sel_table(sql):
        res_data.append(row2[0])


    # tmp_data = dict()
    # for row2 in MySql.sel_table(sql):
    #     if tmp_data.get(row2[0]) is None:
    #         tmp_data[row2[0]] = dict()
    #     if tmp_data.get(row2[0]).get(row2[1]) is None:
    #         tmp_data[row2[0]][row2[1]] = dict()
    #     if tmp_data.get(row2[0]).get(row2[1]).get(row2[2]) is None:
    #         tmp_data[row2[0]][row2[1]][row2[2]] = []
    #     tmp_data[row2[0]][row2[1]][row2[2]].append({
    #         'value': row2[3],
    #         'label': row2[3]
    #     })
    # 
    # 
    # res_data = []
    # for country in tmp_data:
    #     c = {
    #         'value': country,
    #         'label': country,
    #         'children': []
    #     }
    #     res_data.append(c)
    #     for prov in tmp_data[country]:
    #         p = {
    #             'value': prov,
    #             'label': prov,
    #             'children': []
    #         }
    #         c['children'].append(p)
    # 
    #         for grop in tmp_data[country][prov]:
    #             g = {
    #                 'value': grop,
    #                 'label': grop,
    #                 'children': []
    #             }
    #             p['children'].append(g)
    #             g['children'] = tmp_data[country][prov][grop]

    return HttpResponse(json.dumps(res_data, indent=2, ensure_ascii=False))




class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FieldFile):
            if hasattr(obj, 'url'):
                return obj.url
            else:
                return ''
        return json.JSONEncoder.default(self, obj)
