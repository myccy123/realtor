# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from app.models import *
from utils import jsonutil
from utils import dateutil
from web.models import *
from singlepage.models import *
from models import *
from news.models import *
from singlepage.models import *
from common.response import *
from common.decorations import *
from myweb.itools import *
import time
import requests

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

# Create your views here.

def get_count(request):
    cnt = dict()
    cnt['listing'] = Listing.objects.filter(
        datadate__gte=dateutil.add_days(dateutil.now(), -7)).count()
    if cnt['listing'] == 0:
        cnt['listing'] = 1680
    cnt['agent'] = agent_info.objects.filter(active='1').count()
    cnt['estate'] = 16
    return HttpResponse(success(cnt))


def agent_list(request):
    agents = []

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
                        and a.head <> 'agentimgs/def_head.png'
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
                        CASE WHEN a.username2 <> '' THEN 1 ELSE 0 END DESC limit 16"""):
        jsn = dict()
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
        agents.append(jsn)
    return HttpResponse(success(agents))


def listing_list(request):
    CODE_MAP = {
        'no': '在售',
        'yes': '已售',
        'rent': '出租',
        'rented': '已租',
        'presale': '楼花',
        'dark': '暗盘',
        'invalid': '未升效',
    }

    listings = []
    od = Systemorder.objects.filter(status='completed',
                                    ordertype__in=['listing1', 'sale',
                                                   'listing2', 'rent',
                                                   'mysite']).order_by(
        '-starttime')
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
            if s.salestatus == 'invalid':
                continue
            listingid = s.listingid
            sharetype = o.ordertype
            token = Tokens.objects.get(token=s.token)
            ui = agent_info.objects.get(userid=token.userid)
            uid = ui.id
            username = ui.username
            usercity = get_cityname(ui.city)
            corp = 'Webmainland Single Website'
            head = ui.head.url
        jsn = dict()
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
            jsn['listingtype'] = '在售'
            jsn['addr'] = li.listingname
            jsn['price'] = li.price
            jsn['areas'] = li.areas
            jsn['bedroom'] = li.bedroom
            jsn['bashroom'] = li.toilet
            jsn['cityname'] = get_cityname(li.cityname)
            jsn['housetype'] = get_housetype_name(li.housetype)
            jsn['visit'] = s.visit
            jsn['good'] = s.good
            jsn['date'] = s.sharetime.strftime('%Y-%m-%d')
            jsn['htmlid'] = '/web/listing1/' + li.listingid
            listings.append(jsn)
        elif sharetype == 'sale':
            jsn['mls'] = s.listingid
            jsn['listingname'] = s.listingname
            jsn['listingtype'] = CODE_MAP.get(s.salestatus)
            jsn['addr'] = s.listingname
            jsn['bedroom'] = s.bedroom
            jsn['bashroom'] = s.toilet
            jsn['price'] = s.price
            jsn['corp'] = s.listingtype
            jsn['areas'] = s.areas if s.areas.strip() != '' else '-- sqft.'
            jsn['cityname'] = get_cityname(s.cityname)
            jsn['housetype'] = get_housetype_name(s.housetype)
            jsn['visit'] = s.visit
            jsn['good'] = s.good
            jsn['date'] = s.datadate.strftime('%Y-%m-%d')
            jsn['htmlid'] = s.url
            listings.append(jsn)

    his = Access_hitory(addr=request.META.get('REMOTE_ADDR', ''),
                        actiontype='query', htmltype='index',
                        agent=request.META.get('HTTP_USER_AGENT', '')
                        , referer=request.META.get('HTTP_REFERER', 'url'))
    his.save()
    return HttpResponse(success(listings))


def friend_corps(request):
    corps = FriendCorp.objects.all()
    res_data = serialize(corps)
    return HttpResponse(success(res_data))


def article_list(request):
    atc = Article_info.objects.filter(id__in=(2523, 2595))
    atcs = []
    for a in atc:
        tmp = dict()
        tmp['id'] = a.id
        tmp['title'] = a.title
        tmp['intro'] = a.instr
        tmp['img'] = a.img.url
        tmp['url'] = 'http://www.realtoraccess.com/news/%s' % a.id
        atcs.append(tmp)
    return HttpResponse(success(atcs))


def agent_detail(request, uid):
    user = agent_info.objects.get(id=uid)
    res_data = serialize(user)
    res_data['cityName'] = get_cityname(res_data['city'])

    if res_data['tel'] == '':
        res_data['tel'] = '400 877 1896'
    if res_data['email'] == '':
        res_data['email'] = 'info@realtoraccess.com'
    if res_data['note'] == '':
        res_data['note'] = '海外房产投资估价'
    if res_data['corp'] == '':
        res_data['corp'] = '大温专业房产经纪人'
    if res_data['selfintro'] == '':
        res_data[
            'selfintro'] = '欢迎您来我的中文网站，我是一名专业的海外房产经纪人。在这里您将看到我的介绍，我所代理的特色房源和我的团队介绍，无论您是首次置业者或者专业的海外房产投资人，或者要售出您的房屋，我都能为您提供全程房屋买售服务与专业的海外房产置业方案。'
    if res_data['corpintro'] == '':
        res_data[
            'corpintro'] = '海外瑞安居（简称“瑞安居”，RealtorAccess），面向全球华人买家和卖家，提供最及时的房产投资资讯、最高效的房源推广展示以及最专业的房产经纪人推荐。除MLS房源信息外，更汇集了学区房、楼花暗盘、商业地产以及潜力投资房源信息，让全球华人可以查询海外主要城市房价、实时跟踪海外房源价格走势，确保房产投资回报。'
    if res_data['teamintro'] == '':
        res_data[
            'teamintro'] = '海外瑞安居（简称“瑞安居”，RealtorAccess）集成视频、3D、户型图以及房源照片等房源详情信息，通过地图方式全面动态展示最新公众开放日信息。海外华人卖家选择海外瑞安居进行线上挂盘，平台将为您匹配最专业的房产经纪人，无论您身在何方，都有专人为您提供专属定制营销推广服务，您的房产挂牌信息可直达海外房产投资的潜力买家，实现快速高效售房。海外瑞安居是全球海外房产投资者进行海外房产置业投资的不二选择。'

    if agent_auth.objects.filter(userid=user.userid, status='paid',
                                 service='auth'):
        res_data['auth'] = True
    else:
        res_data['auth'] = False

    if not res_data['auth'] or 'agentimgs/def_qrcode.png' in res_data['qrcode']:
        res_data['qrcode'] = 'http://www.realtoraccess.com/data/agentimgs/yvropenhouse.jpg'
    if not res_data['auth'] or 'agentimgs/def_qrcode.png' in res_data[
        'qrcode2']:
        res_data['qrcode2'] = 'http://www.realtoraccess.com/data/agentimgs/yvropenhouse.jpg'

    if res_data['auth'] and res_data['selfintro_cn'] != '':
        res_data['selfintro'] = res_data['selfintro_cn']
    if res_data['auth'] and res_data['corpintro_cn'] != '':
        res_data['corpintro'] = res_data['corpintro_cn']
    if res_data['auth'] and res_data['teamintro_cn'] != '':
        res_data['teamintro'] = res_data['teamintro_cn']

    res_data['corpVideo'] = ''
    res_data['agentImgs'] = []
    imgs = agent_img.objects.filter(userid=user.userid)
    for img in imgs:
        if img.imgtype == 'agent':
            res_data['agentImgs'].append(img.img.url)
        elif img.imgtype == 'video':
            res_data['corpVideo'] = img.img.url

    res_data['visit'] = Access_hitory.objects.filter(htmltype='agenthome',
                                                     userid=user.userid).count()
    return HttpResponse(success(res_data))


def chinese_service(request):
    body = jsonutil.loads(request.body)
    userid = body.get('userid', '')
    custname = body.get('custname', '')
    custemail = body.get('custemail', '')
    custmsg = body.get('custmsg', '')

    user_info = agent_info.objects.get(userid=userid)
    custmsg += '\nhttp://www.realtoraccess.com/web/agent/%s' % user_info.id

    mls = body.get('mls', '')
    mail_api('C', userid, custemail, custname, custmsg)
    msg = cust_message(userid=userid, custname=custname, custemail=custemail,
                       custmsg=custmsg, mls=mls)
    msg.save()
    someone_leave_msg(userid)
    return HttpResponse(success())


def get_status_name(code):
    name_map = dict()
    name_map['no'] = '在售'
    name_map['yes'] = '已售'
    name_map['rent'] = '出租'
    name_map['rented'] = '已租'
    name_map['presale'] = '楼花'
    name_map['dark'] = '暗盘'
    name_map['invalid'] = '未升效'
    return name_map.get(code, '在售')


def agent_listings(request):
    agnet_id = request.GET.get('id')
    order_by = request.GET.get('sort', '-date')
    desc_asc = 'desc' if '-' in order_by else 'asc'
    d_a = '-' if '-' in order_by else ''
    user = agent_info.objects.get(id=agnet_id)
    tks = Tokens.objects.filter(userid=user.userid)
    tokens = [t.token for t in tks]
    if 'date' in order_by:
        ls = Listing_for_sp.objects.filter(token__in=tokens).order_by(
            d_a + 'datadate')
    elif order_by == 'price':
        ls = Listing_for_sp.objects.raw("""
                    SELECT *
                    FROM app.`singlepage_listing_for_sp`
                    WHERE token IN (SELECT token FROM app.`singlepage_tokens` WHERE userid = '%s')
                    ORDER BY CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) %s
            """ % (user.userid, desc_asc))
    elif order_by == 'visit':
        ls = Listing_for_sp.objects.filter(token__in=tokens).order_by(
            d_a + 'visit')
    else:
        return HttpResponse(error('01', '参数错误!'))

    lsts = []
    for l in ls:
        if l.salestatus == 'invalid':
            continue
        tmp = dict()
        tmp['mls'] = l.listingid
        tmp['url'] = l.url
        tmp['url2'] = 'http://realtoraccess.com/sp/smart/flyer1/%s/?token=%s' % (l.listingid, l.token)
        if l.sptype == 'custom':
            tmp['url2'] = l.url

        tmp['htmlid'] = l.url
        tmp['price'] = l.price
        tmp['address'] = l.listingname
        tmp['areas'] = l.areas
        tmp['bedroom'] = l.bedroom
        tmp['toilet'] = l.toilet
        tmp['housetype'] = get_housetype_name(l.housetype)
        tmp['visit'] = l.visit
        tmp['cityname'] = l.cityname if l.distid == '' else get_cityname(
            l.distid)
        tmp['date'] = l.datadate.strftime('%Y-%m-%d')
        tmp['salestatus'] = l.salestatus
        tmp['salestatus_name'] = get_status_name(l.salestatus)
        tmp['sptype'] = l.sptype
        tmp['token'] = l.token
        tmp['img'] = ''
        for i in Listingimg.objects.filter(listingid=l.listingid):
            tmp['img'] = i.img.url
            break
        if l.sptype == 'smf':
            lsts.append(tmp)
        elif l.sptype == 'custom':
            for i in Listingimg.objects.filter(listingid=l.listingid):
                if 'from_addlisting.jpg' in i.imgname:
                    tmp['img'] = i.img.url
                    break
            lsts.append(tmp)
    return HttpResponse(success(lsts))


def listing_info(request):
    mls = request.GET.get('mls')
    listing = Listing.objects.get(listingid=mls)

    limgs = Listingimg.objects.filter(listingid=mls, imgtype='listing1')
    imgs = []
    for img in limgs:
        imgs.append(img.img.url)
    res_data = serialize(listing)
    res_data['imgs'] = imgs
    return HttpResponse(success(res_data))


def commit_email(request):
    body = jsonutil.loads(request.body)
    MessageCenter.objects.create(msg_type=body.get('type', 'agent_page_4'),
                                 agentid=body.get('userId', ''),
                                 mls=body.get('mls', ''),
                                 user_name=body.get('name', ''),
                                 user_msg=body.get('msg', ''),
                                 user_email=body.get('email', ''),
                                 user_tel=body.get('tel', ''),
                                 src_url=body.get('url', ''),
                                 user_ip=request.META.get('REMOTE_ADDR'))
    if body.get('type', 'agent_page_4') == "smart_flyer_2":
        mail_api('E', body.get('userId', ''), body.get('email', ''),
                 body.get('name', ''), body.get('msg', '') + '\n' + body.get('url', ''), body.get('tel', ''))
    elif body.get('type', 'agent_page_4') == "agent_page_4":
        mail_api('D', body.get('userId', ''), body.get('email', ''),
                 body.get('name', ''),
                 body.get('msg', '') + '\n' + body.get('url', ''),
                 body.get('tel', ''))
    return HttpResponse(success())


def get_crumbs(request):
    city = request.GET.get('city')
    sql = "select countryname,provname,groupname,cityname,countyname,countryid,provid,groupid,cityid,countyid from app.t99_cityname where srcdata='%s' " % city
    crumbs = dict()
    for row in MySql.sel_table(sql):
        crumbs['country'] = row[0]
        crumbs['prov'] = row[1]
        crumbs['group'] = row[2]
        crumbs['city'] = row[3]
        crumbs['county'] = row[4]
        crumbs['countryid'] = row[5]
        crumbs['provid'] = row[6]
        crumbs['groupid'] = row[7]
        crumbs['cityid'] = row[8]
        crumbs['countyid'] = row[9]
    return HttpResponse(success(crumbs))


def get_nearby(request):
    city = request.GET.get('city')

    dicts = []
    mycountyid = ''
    mycityid = ''
    mygroupid = ''

    nearby_county = []
    nearby_city = []
    for row in MySql.sel_table("select * from app.t99_cityname"):
        dicts.append(row)
    for d in dicts:
        if d[10].lower() == city.lower():
            mycountyid = d[0]
            mycityid = d[2]
            mygroupid = d[4]
            break

    for d in dicts:
        if d[2] == mycityid and d[0] != mycountyid:
            url = '/web/houses/all-all-%s-%s-%s-all-all-all-all-1' % (
                d[4], d[2], d[0])
            nearby_county.append([d[0], d[1], url])
    for d in dicts:
        if d[4] == mygroupid and d[2] != mycityid:
            url = '/web/houses/all-all-%s-%s-all-all-all-all-all-1' % (
                d[4], d[2])
            nearby_city.append([d[2], d[3], url])

    if len(nearby_county) == 0:
        res_data = {'nearlev': 'city', 'nearby': nearby_city}
    else:
        res_data = {'nearlev': 'county', 'nearby': nearby_county}

    return HttpResponse(success(res_data))


@http_log()
def get_agent_of_listing(request):
    mls = request.GET.get('mls')

    # single page listing
    try:
        listing = Listing_for_sp.objects.get(listingid=mls)
        tk = Tokens.objects.get(token=listing.token)
        user = agent_info.objects.get(userid=tk.userid)
        return HttpResponse(success(serialize(user)))
    except Listing_for_sp.DoesNotExist:
        pass

    # 12 URL
    listing = Listing.objects.get(listingid=mls)
    if listing.cityname in (
            'Vancouver', 'WestVan', 'Burnaby', 'Surrey', 'Coquitlam',
            'whiterock',
            'PortMoody', 'Richmond', 'NorthVancouver', 'NorthSurrey',
            'newWestminster',
            'Whistler'):
        city_map = {
            'Vancouver': 'yaletownrealtor@gmail.com',
            'WestVan': 'michellevaughan@shaw.ca',
            'Burnaby': 'mwtsang@aol.com',
            'Surrey': 'chris@chrisdavidson.ca',
            'Coquitlam': 'zachtchester@gmail.com',
            'whiterock': 'E.dave@davesnider.ca',
            'PortMoody': 'colin@colindavidson.ca',
            'Richmond': 'haileycc0127@gmail.com',
            'NorthVancouver': 'info@titacool.com',
            'NorthSurrey': 'mnicolsrealty@gmail.com',
            'newWestminster': 'billwan.re@gmail.com',
            'Whistler': 'brenda@brendarussell.ca'
        }
        user = agent_info.objects.get(userid=city_map[listing.cityname])
        return HttpResponse(success(serialize(user)))

    # other
    user_pool = agent_info.objects.filter(active='1')
    lid = int(time.mktime(listing.datadate.timetuple()))
    idx = lid % len(user_pool)
    user = user_pool[idx]

    res_data = serialize(user)
    if res_data['tel'] == '':
        res_data['tel'] = '400 877 1896'
    if res_data['email'] == '':
        res_data['email'] = 'info@realtoraccess.com'
    if res_data['note'] == '':
        res_data['note'] = '海外房产投资估价'
    if res_data['corp'] == '':
        res_data['corp'] = '大温专业房产经纪人'
    res_data['city'] == get_cityname(res_data['city'])

    return HttpResponse(success(res_data))


def get_recommend_listings(request):
    mls = request.GET.get('mls')
    page = int(request.GET.get('page', '1'))
    page_size = int(request.GET.get('page_size', '4'))

    res_data = []
    try:
        ls = Listing.objects.get(listingid=mls)
    except Listing.DoesNotExist:
        return HttpResponse(error('01', 'mls invaid!'))

    open_houses = Openhouse.objects.filter(
        Q(bgndate1__date__gte=dateutil.now()) | Q(
            bgndate2__date__gte=dateutil.now()))
    open_mls = [l.listingid for l in open_houses]
    open_listings = Listing_for_sp.objects.filter(listingid__in=open_mls)
    for opls in open_listings:
        if opls.cityname == ls.cityname and opls.salestatus != 'invalid':
            res_data.append(opls)

    near_ls = Listing.objects.filter(cityname=ls.cityname).order_by('-datadate')
    lmt = page * page_size + 100
    for nl in near_ls[:lmt]:
        res_data.append(nl)

    p = Paginator(res_data, page_size)
    data = serialize(p.page(page).object_list)
    for d in data:
        imgs = [img.img.url for img in
                Listingimg.objects.filter(listingid=d['listingid'])]
        d['imgs'] = imgs

        if d.get('token') is None:
            d['htmlid'] = '/web/listing1/' + d['listingid']
        else:
            d['htmlid'] = d['url']

    return HttpResponse(success(data))


def city_avg_price(request):
    res_data = [
        {
            'city': 'Vancouver',
            'cityName': '温哥华',
            'url': 'http://www.realtoraccess.com/web/van/',
        },
        {
            'city': 'WestVan',
            'cityName': '西温哥华',
            'url': 'http://www.realtoraccess.com/web/westvan/',
        },
        {
            'city': 'Burnaby',
            'cityName': '本拿比',
            'url': 'http://www.realtoraccess.com/web/burnaby/',
        },
        {
            'city': 'Surrey',
            'cityName': '素里',
            'url': 'http://www.realtoraccess.com/web/surrey/',
        },
        {
            'city': 'Coquitlam',
            'cityName': '高贵林',
            'url': 'http://www.realtoraccess.com/web/coquitlam/',
        },
        {
            'city': 'WhiteRock',
            'cityName': '白石',
            'url': 'http://www.realtoraccess.com/web/whiterock/',
        },
        {
            'city': 'PortMoody',
            'cityName': '满地宝',
            'url': 'http://www.realtoraccess.com/web/portmoody/',
        },
        {
            'city': 'Richmond',
            'cityName': '列治文',
            'url': 'http://www.realtoraccess.com/web/richmond/',
        },
        {
            'city': 'NorthVancouver',
            'cityName': '北温',
            'url': 'http://www.realtoraccess.com/web/northvan/',
        },
        {
            'city': 'NorthSurrey',
            'cityName': '北素里',
            'url': 'http://www.realtoraccess.com/web/northsurrey/',
        },
        {
            'city': 'NewWestminster',
            'cityName': '新西敏',
            'url': 'http://www.realtoraccess.com/web/newwestminster/',
        },
        {
            'city': 'Whistler',
            'cityName': '惠斯勒',
            'url': 'http://www.realtoraccess.com/web/whistler/',
        },
    ]
    return HttpResponse(success(res_data))


def new_listings(request):
    mls = request.GET.get('mls')
    try:
        ls = Listing.objects.get(listingid=mls)
    except Listing.DoesNotExist:
        return HttpResponse(error('01', 'mls invaid!'))
    newls = Listing.objects.filter(cityname=ls.cityname,
                                   datadate__gte=dateutil.add_days(
                                       dateutil.now(), -30))
    res_data = []
    for l in newls[:12]:
        res_data.append(serialize(l))

    if len(res_data) < 12:
        cityls = Listing_for_sp.objects.filter(cityname=ls.cityname)
        cityls = serialize(cityls)
        res_data += cityls

    return HttpResponse(success(res_data[:12]))


def smart_flyer(request):
    mls = request.GET.get('mls')
    token = request.GET.get('token')

    if 'realtoraccesssupertoken' in token:
        token = 'realtoraccesssupertoken'
    else:
        token = token[0:15]

    try:
        sp = Listing_for_sp.objects.get(listingid=mls, token=token)
        sp.visit += 1
        sp.save()
    except Listing_for_sp.DoesNotExist:
        return HttpResponse(error('01', 'mls or token invalid!'))

    Flow_statistics.objects.create(addr=request.META['REMOTE_ADDR'],
                                   htmlid='%s_%s' % (mls, token), htmltype='sp',
                                   agent=request.META['HTTP_USER_AGENT']
                                   , referer=request.META.get('HTTP_REFERER',
                                                              'url'))
    userid = Tokens.objects.get(token=token).userid
    medias = Sp_img.objects.filter(listingid=mls)
    listing_imgs = Listingimg.objects.filter(listingid=mls)
    media = dict()
    media['imgs'] = []
    media['hx'] = []
    media['video'] = []
    media['pdf'] = []
    media['bgimg1'] = []
    media['bgimg2'] = []
    media['bgimg3'] = []
    media['bgimg4'] = []
    media['preimg'] = []

    for v in medias:
        if v.imgtype == 'hx' and v.owner in ('', userid):
            media['hx'].append(v.img.url)
        if v.imgtype == 'video' and v.owner in ('', userid):
            media['video'] = v.img.url
        if v.imgtype == 'pdf' and v.owner in ('', userid):
            media['pdf'] = v.img.url
        if v.imgtype == 'bgimg1' and v.owner in ('', userid):
            media['bgimg1'] = v.img.url
        if v.imgtype == 'bgimg2' and v.owner in ('', userid):
            media['bgimg2'] = v.img.url
        if v.imgtype == 'bgimg3' and v.owner in ('', userid):
            media['bgimg3'] = v.img.url
        if v.imgtype == 'bgimg4' and v.owner in ('', userid):
            media['bgimg4'] = v.img.url
        if v.imgtype == 'preimg' and v.owner in ('', userid):
            media['preimg'] = v.img.url

    for img in listing_imgs:
        media['imgs'].append(img.img.url)

    # OPEN HOUSE
    open_houses = []
    oh = Openhouse.objects.filter(listingid=mls)
    for open_house in oh:
        tmp1 = []
        if open_house.bgndate1 is not None and open_house.bgndate1 > dateutil.now():
            tmp1.append(dateutil.format_datetime(open_house.bgndate1, '%m月%d日 %H:%M'))
        if open_house.enddate1 is not None and open_house.enddate1 > dateutil.now():
            tmp1.append(dateutil.format_datetime(open_house.enddate1, '%m月%d日 %H:%M'))
        if ' 至 '.join(tmp1) != '':
            open_houses.append(' 至 '.join(tmp1))
        tmp2 = []
        if open_house.bgndate2 is not None and open_house.bgndate2 > dateutil.now():
            tmp2.append(dateutil.format_datetime(open_house.bgndate2, '%m月%d日 %H:%M'))
        if open_house.enddate2 is not None and open_house.enddate2 > dateutil.now():
            tmp2.append(dateutil.format_datetime(open_house.enddate2, '%m月%d日 %H:%M'))
        if ' 至 '.join(tmp2) != '':
            open_houses.append(' 至 '.join(tmp2))

    res_data = serialize(sp)
    res_data['intro'] = res_data['intro_zh'] if res_data['intro_zh'] != '' else res_data['intro']
    res_data['media'] = media
    res_data['userid'] = userid
    res_data['agentId'] = agent_info.objects.get(userid=userid).id
    res_data['open_house'] = open_houses
    return HttpResponse(success(res_data))
