# -*- coding:utf-8 -*-
from app.models import *
from singlepage.models import *
from django.shortcuts import HttpResponse, render_to_response, redirect
from myweb.itools import *
from mail_template import *
from PIL import Image
import os
from web.models import agent_info, agent_card, agent_auth
from portal.models import MessageCenter


def index(request, mls):
    token = request.GET.get('token')
    if 'realtoraccesssupertoken' in token:
        token = 'realtoraccesssupertoken'
    else:
        token = token[0:15]

    l = Listing_for_sp.objects.get(listingid=mls, token=token)
    l.visit += 1
    l.save()

    presell = '1' if l.listingid[-1] == 'y' else '0'
    bed = l.bedroom[0] if l.bedroom <> '' else '0'
    tol = l.toilet[0] if l.toilet <> '' else '0'
    addr = ''
    pname = ''
    if presell == '1':
        bed = l.bedroom
        tol = l.toilet

        if len(l.listingname.split('@')) == 2:
            (addr, pname) = l.listingname.split('@')
        else:
            addr = l.listingname
            pname = l.listingname

    fs = Flow_statistics(addr=request.META['REMOTE_ADDR'],
                         htmlid='%s_%s' % (mls, token), htmltype='sp',
                         agent=request.META['HTTP_USER_AGENT']
                         , referer=request.META.get('HTTP_REFERER', 'url'))
    fs.save()
    look = Flow_statistics.objects.filter(
        htmlid__icontains='%s_%s' % (mls, token)).count()
    tk = Tokens.objects.get(token=token, active='1')
    u = agent_info.objects.get(userid=tk.userid)

    # if agent_auth.objects.filter(userid=tk.userid,
    #                              status='paid',
    #                              service='diyPage'):
    #     return redirect('/sp/smart/flyer1/%s/?token=%s' % (mls, token), permanent=True)

    sql = "select * from app.t00_listing_coagent where token = '%s' " % token
    for row in MySql.sel_table(sql):
        u.username2 = row[1] + ' ' + row[2]
        u.tel2 = row[3]
        u.email2 = row[4]
        u.qrcode2 = row[5]
        u.head2 = row[6]

    vdo = Sp_img.objects.filter(listingid=mls)
    video = ''
    pdf = ''
    bgimg1 = ''
    bgimg2 = ''
    bgimg3 = ''
    bgimg4 = ''
    preimg = ''
    for v in vdo:
        if v.imgtype == 'video' and v.owner in ('', tk.userid):
            video = v.img.url
        if v.imgtype == 'pdf' and v.owner in ('', tk.userid):
            pdf = v.img.url
        if v.imgtype == 'bgimg1' and v.owner in ('', tk.userid):
            bgimg1 = v.img.url
        if v.imgtype == 'bgimg2' and v.owner in ('', tk.userid):
            bgimg2 = v.img.url
        if v.imgtype == 'bgimg3' and v.owner in ('', tk.userid):
            bgimg3 = v.img.url
        if v.imgtype == 'bgimg4' and v.owner in ('', tk.userid):
            bgimg4 = v.img.url
        if v.imgtype == 'preimg' and v.owner in ('', tk.userid):
            preimg = v.img.url

    res = render_to_response('sp/index.html',
                             {'l': l, 'user': u, 'bed': bed, 'tol': tol,
                              'video': video, 'pdf': pdf, 'presell': presell,
                              'addr': addr, 'pname': pname,'latlng': [l.lat, l.lng],
                              'bgimg1': bgimg1, 'bgimg2': bgimg2,
                              'bgimg3': bgimg3, 'bgimg4': bgimg4,
                              'preimg': preimg, 'look': look})
    res['X-Frame-Options'] = 'ALLOWALL'

    return res


def single_page_bi(request):
    mls = request.GET.get('mls')
    token = request.GET.get('token')

    # all listing of user
    userid = Tokens.objects.get(token=token).userid
    tokens = Tokens.objects.filter(userid=userid)
    alltoken = [t.token for t in tokens]
    alllisting = Listing_for_sp.objects.filter(token__in=alltoken)

    # personal url
    purl = ''
    sql = "select url from app.singlepage_personal_url where mls='%s' " % mls
    for row in MySql.sel_table(sql):
        purl = row[0]

    createdate = ''
    for thislisting in alllisting:
        if token == thislisting.token:
            createdate = thislisting.datadate

    finfo = {}
    ivc = ''
    try:
        card = agent_card.objects.get(userid=userid, cardtype='1')
        finfo['holder'] = card.holder
        finfo['cardno'] = card.cardno
        finfo['yyyy'] = card.expire.split('/')[0]
        finfo['mm'] = card.expire.split('/')[1]
        finfo['cvs'] = card.cvs
        finfo['postid'] = card.postid
    except agent_card.DoesNotExist:
        finfo['holder'] = ''
        finfo['cardno'] = ''
        finfo['yyyy'] = ''
        finfo['mm'] = ''
        finfo['cvs'] = ''
        finfo['postid'] = ''

    try:
        auth = agent_auth.objects.get(token=token)
        finfo['status'] = auth.status
        if hasattr(auth.invoice, 'url'):
            ivc = auth.invoice.url

    except agent_auth.DoesNotExist:
        finfo['status'] = 'not paid'

    bi = BI_map.objects.filter(mls=mls, token=token).order_by('orderid')
    chartid = []
    for i in bi:
        chartid.append(i.template_id)
    return render_to_response('sp/sp_bi.html',
                              {'chartid': chartid, 'alllisting': alllisting,
                               'finfo': finfo, 'mls': mls, 'token': token,
                               'purl': purl
                                  , 'ivc': ivc, 'createdate': createdate,
                               'userid': userid})


def post_credit_card(request):
    mls = request.POST.get('mls')
    token = request.POST.get('token')
    name = request.POST.get('name')
    cardid = request.POST.get('cardid')
    yyyy = request.POST.get('yyyy')
    mm = request.POST.get('mm')
    cvs = request.POST.get('cvs')
    postid = request.POST.get('postid')

    try:
        userid = Tokens.objects.get(mls=mls, token=token).userid
        for f in agent_card.objects.filter(userid=userid):
            f.cardtype = 0
            f.save()

        cur = agent_card(userid=userid, holder=name, cardno=cardid,
                         expire=yyyy + '/' + mm, cvs=cvs, postid=postid,
                         cardtype='1')
        cur.save()
        return HttpResponse('ok')
    except Tokens.DoesNotExist:
        return HttpResponse('token err!')


def make_preimg(request):
    listingid = request.GET.get('mls')
    tx = request.GET.get('x')
    ty = request.GET.get('y')
    bg1 = Sp_img.objects.get(listingid=listingid, imgtype='bgimg1')

    srcimg = '/root/myweb/data/' + bg1.img.name
    img = Image.open(srcimg)
    if tx != None and ty != None:
        x = 0
        y = 0
        w = int(tx)
        h = int(ty)
    else:
        if img.size[0] <= 1200:
            x = 0
            w = img.size[0]
        else:
            x = (img.size[0] - 1200) / 2
            w = 1200

        if img.size[1] <= 630:
            y = 0
            h = img.size[1]
        else:
            y = (img.size[1] - 630) / 2
            h = 630

    #         region = img.crop((x, y, x+w, y+h))
    region = img.resize((w, h), Image.ANTIALIAS)
    #         region.show()
    region.save('/root/myweb/data/sp_imgs/%s_preimg.jpeg' % listingid)
    try:
        Sp_img.objects.get(listingid=listingid, imgtype='preimg')
    except Sp_img.DoesNotExist:
        pi = Sp_img(listingid=listingid, imgtype='preimg',
                    img='sp_imgs/%s_preimg.jpeg' % listingid)
        pi.save()

    return HttpResponse('ok!')


def make_sp(request, token):
    try:
        tk = Tokens.objects.get(token=token)
        listingid = request.GET.get('mls')
        try:
            l = Listing.objects.get(listingid=listingid)
            sp = Listing_for_sp(listingid=l.listingid,
                                listingname=l.listingname, cityname=l.cityname,
                                price=l.price, areas=l.areas, bedroom=l.bedroom,
                                toilet=l.toilet, parking=l.parking, tax=l.tax,
                                housetype=l.housetype, housestyle=l.housestyle,
                                basement=l.basement,
                                builddate=l.builddate, intro=l.intro,
                                goodat=l.goodat, corp=l.corp, warning=l.warning,
                                url='http://' + request.META[
                                    'HTTP_HOST'] + '/sp/listing/%s/?token=%s' % (
                                    listingid, token),
                                intro_zh=translate_en2zh(l.intro),
                                schoolid=l.schoolid, postid=l.postid, lat=l.lat,
                                lng=l.lng, token=token, distid=l.cityname)
            sp.save()
        except Listing.DoesNotExist:
            sp = Listing_for_sp(listingid=request.GET.get('mls'), token=token,
                                url='http://' + request.META[
                                    'HTTP_HOST'] + '/sp/listing/%s/?token=%s' % (
                                    request.GET.get('mls'), token))
            sp.save()

        #         已迁移至新的模型agent_auth
        #         username = ''
        #         cardid = ''
        #         yyyy = ''
        #         mm = ''
        #         cvs = ''
        #         invoice = ''
        #         for f in finance.objects.filter(userid=tk.userid):
        #             if f.username <> '' or f.cardid <> '' or f.yyyy <> '' or f.mm <> '' or f.cvs <> '' or f.invoice <> '':
        #                 username = f.username
        #                 cardid = f.cardid
        #                 yyyy = f.yyyy
        #                 mm = f.mm
        #                 cvs = f.cvs
        #                 invoice = f.invoice
        #                 break
        #
        #         fin = finance(mls=listingid,token=token,userid=tk.userid,username=username,cardid=cardid,yyyy=yyyy,mm=mm,cvs=cvs,invoice=invoice)
        #         fin.save()

        # 已迁移至新的模型Openhouse
        #         try:
        #             Open_house.objects.get(listingid=listingid)
        #         except Open_house.DoesNotExist:
        #             oh = Open_house(listingid=listingid)
        #             oh.save()
        return HttpResponse('single website maked!')

    except Tokens.DoesNotExist, Listing.DoesNotExist:
        return HttpResponse('token deny!')


def make_spread(request, mls):
    try:
        sp = Listing_for_sp.objects.get(listingid=mls)
        tp = 'sale'
        try:
            Systemorder.objects.get(htmlid=sp.id)
            return HttpResponse(
                'SinglePage with mls %s has been spreaded!' % mls)
        except Systemorder.DoesNotExist:
            sysod = Systemorder(htmlid=sp.id, userid='', dataid='',
                                ordertype=tp, status='completed')
            sysod.save()
            return HttpResponse(
                'SinglePage with mls %s is spreading on RA!' % mls)
    except Listing_for_sp.DoesNotExist:
        return HttpResponse('SinglePage with mls %s do not exist!' % mls)


def parse_date(d):
    tmp = {}
    tmp['y'] = d.strftime('%Y')
    tmp['m'] = d.strftime('%m')
    tmp['d'] = d.strftime('%d')
    tmp['h'] = d.strftime('%H')
    tmp['M'] = d.strftime('%M')
    tmp['w'] = d.strftime('%a')
    if tmp['w'] == 'Mon':
        tmp['w'] = '星期一'
    elif tmp['w'] == 'Tue':
        tmp['w'] = '星期二'
    elif tmp['w'] == 'Wed':
        tmp['w'] = '星期三'
    elif tmp['w'] == 'Thu':
        tmp['w'] = '星期四'
    elif tmp['w'] == 'Fri':
        tmp['w'] = '星期五'
    elif tmp['w'] == 'Sat':
        tmp['w'] = '星期六'
    elif tmp['w'] == 'Sun':
        tmp['w'] = '星期日'
    return tmp


def get_openhouse(request):
    mls = request.GET.get('mls')
    try:
        oh = Openhouse.objects.get(listingid=mls)
    except Openhouse.DoesNotExist:
        return HttpResponse(json.dumps([], indent=2, ensure_ascii=False))
    res = []

    # first
    if oh.bgndate1 != None and oh.enddate1 != None:
        bgn = parse_date(oh.bgndate1)
        end = parse_date(oh.enddate1)

        if bgn['y'] + bgn['m'] + bgn['d'] == end['y'] + end['m'] + end['d']:
            res.append({'opendate': '%s年，%s月%s日，%s' % (
            bgn['y'], bgn['m'], bgn['d'], bgn['w'])
                           , 'opentime': '%s:%s - %s:%s' % (
                bgn['h'], bgn['M'], end['h'], end['M'])})
        else:
            res.append({'opendate': '%s年，%s月%s日，%s %s:%s' % (
            bgn['y'], bgn['m'], bgn['d'], bgn['w'], bgn['h'], bgn['M'])
                           , 'opentime': '%s年，%s月%s日，%s %s:%s' % (
                end['y'], end['m'], end['d'], end['w'], end['h'], end['M'])})

    elif oh.bgndate1 != None or oh.enddate1 != None:
        thedate = oh.bgndate1 if oh.bgndate1 != None else oh.enddate1
        the = parse_date(thedate)
        res.append({'opendate': '%s年，%s月%s日，%s' % (
        the['y'], the['m'], the['d'], the['w'])
                       , 'opentime': '%s:%s' % (the['h'], the['M'])})
    # second
    if oh.bgndate2 != None and oh.enddate2 != None:
        bgn = parse_date(oh.bgndate2)
        end = parse_date(oh.enddate2)

        if bgn['y'] + bgn['m'] + bgn['d'] == end['y'] + end['m'] + end['d']:
            res.append({'opendate': '%s年，%s月%s日，%s' % (
            bgn['y'], bgn['m'], bgn['d'], bgn['w'])
                           , 'opentime': '%s:%s - %s:%s' % (
                bgn['h'], bgn['M'], end['h'], end['M'])})
        else:
            res.append({'opendate': '%s年，%s月%s日，%s %s:%s' % (
            bgn['y'], bgn['m'], bgn['d'], bgn['w'], bgn['h'], bgn['M'])
                           , 'opentime': '%s年，%s月%s日，%s %s:%s' % (
                end['y'], end['m'], end['d'], end['w'], end['h'], end['M'])})

    elif oh.bgndate2 != None or oh.enddate2 != None:
        thedate = oh.bgndate2 if oh.bgndate2 != None else oh.enddate2
        the = parse_date(thedate)
        res.append({'opendate': '%s年，%s月%s日，%s' % (
        the['y'], the['m'], the['d'], the['w'])
                       , 'opentime': '%s:%s' % (the['h'], the['M'])})
    return HttpResponse(json.dumps(res, indent=2, ensure_ascii=False))


def get_listing_imgs(request):
    mls = request.GET.get('mls')
    imgs = Listingimg.objects.filter(listingid=mls,
                                     imgtype='listing1').order_by('imgname')

    res = []
    for img in imgs:
        print img.imgname
        tmp = {}
        tmp['img'] = img.img.url.replace('/listings/', '/listings_small/')
        tmp['desc'] = ''
        res.append(tmp)

    return HttpResponse(json.dumps(res, indent=2, ensure_ascii=False))


def get_floor_plan(request):
    mls = request.GET.get('mls')
    imgs = Sp_img.objects.filter(listingid=mls, imgtype='hx')
    res = []
    if len(imgs) == 0:
        res.append('/static/sp/img/deffloorplan.jpg')
    else:
        for img in imgs:
            res.append(img.img.url)
    return HttpResponse(json.dumps(res, indent=2, ensure_ascii=False))


def call_agent(request):
    mls = request.POST.get('mls')
    url = request.POST.get('url')
    agentid = request.POST.get('agentid')
    name = request.POST.get('name')
    tel = request.POST.get('tel')
    email = request.POST.get('email')
    desc = request.POST.get('desc')
    ip = request.META.get('REMOTE_ADDR')

    desc += '\n' + url
    mail_api('E', agentid, email, name, desc, tel)
    ca = MessageCenter(mls=mls, agentid=agentid, user_name=name, user_tel=tel,
                       user_email=email, user_msg=desc, user_ip=ip,
                       msg_type='smf')
    ca.save()
    cust_msg(agentid, {'name': name, 'url': url, 'tel': tel, 'email': email,
                       'msg': desc})
    return HttpResponse('0')


def home_page(request):
    fs = Flow_statistics(addr=request.META['REMOTE_ADDR'], htmltype='index',
                         agent=request.META['HTTP_USER_AGENT']
                         , referer=request.META.get('HTTP_REFERER', 'url'))
    fs.save()
    return render_to_response('sp_index/index.html')


def get_start(request):
    fname = request.POST.get('fname', '')
    lname = request.POST.get('lname', '')
    email = request.POST.get('email', '')
    mls = request.POST.get('mls', '')
    tel = request.POST.get('tel', '')
    corp = request.POST.get('corp', '')
    address = request.POST.get('address', '')
    postid = request.POST.get('postid', '')
    od = Order_from_website(fname=fname, lname=lname, email=email, mls=mls,
                            tel=tel, corp=corp, address=address, postid=postid)
    od.save()
    send_sp_getstart(
        {'fname': fname, 'lname': lname, 'email': email, 'mls': mls, 'tel': tel,
         'corp': corp, 'address': address, 'postid': postid})
    return HttpResponse('0')


def sign_up(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    try:
        User_information.objects.get(email=email)
        return HttpResponse('Your information was posted!')
    except User_information.DoesNotExist:
        u = User_information(email=email, username=name)
        u.save()
        send_sp_signup({'name': name, 'email': email})
        return HttpResponse('0')


def make_small_listing_imgs(request):
    mls = request.GET.get('mls')
    imgs = Listingimg.objects.filter(listingid=mls, imgtype='listing1')
    target_width = 400
    os.chdir('/root/myweb/data/')
    for i in imgs:
        filename = i.img.name
        filename = os.path.abspath(filename)
        basename = os.path.basename(filename)
        smallname = os.path.join(os.path.dirname(os.path.dirname(filename)),
                                 'listings_small', basename)
        #         if os.path.exists(smallname):
        #             print '%s already smalled!' % filename
        #             continue

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

    return HttpResponse('ok')


def send_mp_message(request):
    token = request.GET.get('token')
    ls = Listing_for_sp.objects.get(token=token)
    MySql.run_sql(
        "INSERT INTO `app`.`t00_mp_message` values(null,'newsp','0','%s','',now())" % ls.listingid)
    return HttpResponse('ok')


def page_smart_flyer(request, mls):
    token = request.GET.get('token')
    ls = Listing_for_sp.objects.get(listingid=mls)
    # if not agent_auth.objects.filter(userid=Tokens.objects.get(token=token).userid,
    #                                  status='paid',
    #                                  service='diyPage'):
    #     return redirect('/sp/listing/%s/?token=%s' % (mls, token), permanent=True)

    fs = Flow_statistics(addr=request.META['REMOTE_ADDR'],
                         htmlid='%s_%s' % (mls, token), htmltype='sp2',
                         agent=request.META['HTTP_USER_AGENT']
                         , referer=request.META.get('HTTP_REFERER', 'url'))
    fs.save()
    return render_to_response('sp/smf1/template/index2.html', {'ls': ls})
