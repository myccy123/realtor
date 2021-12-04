# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponse,render_to_response
from django.db.models import Q
from myweb.itools import *
from mall.models import *
import xml.dom.minidom
from itertools import product
import uuid


def get_webtoken(code):
    params = {}
    params['grant_type'] = 'authorization_code'
    params['appid'] = 'wxe530c431696402d0'
    params['secret'] = 'b8325c44d50e42eb8410f63333d52b50'
    params['code'] = code
    res = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token',params=params)
    print res.json()
    return (res.json()['access_token'],res.json()['openid'])

def get_wx_userinfo(toekn,openid):
    params = {}
    params['access_token'] = toekn
    params['openid'] = openid
    params['lang'] = 'zh_CN'
    res = requests.get('https://api.weixin.qq.com/sns/userinfo',params=params)
    res.encoding = 'utf-8'
    info = res.json()
    try:
        u = Wechat_user_info.objects.get(openid=info.get('openid'))
        u.nickname = info.get('nickname')
        u.headimgurl = info.get('headimgurl')
        u.save()
    except Wechat_user_info.DoesNotExist:
        u = Wechat_user_info(openid=info.get('openid'),nickname=info.get('nickname'),headimgurl=info.get('headimgurl'),sex=info.get('sex'),city=info.get('city')
                         ,province=info.get('province'),country=info.get('country'),language=info.get('language'))
        u.save()
    return info

def product_detail(request):
    pid = request.GET.get('pid')
    code = request.GET.get('code')
    
    islogin = '0'
    userinfo = {}
    
    cuid = request.COOKIES.get('uid','')
    cnickname = request.COOKIES.get('nickname')
    chead = request.COOKIES.get('head')
    
    print request.COOKIES
    
    if len(cuid) > 10: 
        islogin = '1'
        userinfo['openid'] = cuid
        userinfo['head'] = chead
        userinfo['nickname'] = cnickname
    
    elif code:
        (toekn,openid) = get_webtoken(code)
        userinfo = get_wx_userinfo(toekn,openid)
        islogin = '1'
    try:
        pinfo = Product_info.objects.get(product_id=pid)
        pset = Product_sets.objects.filter(product_id=pid)
        pdtl = Product_detail.objects.filter(product_id=pid)
    except Product_info.DoesNotExist:
        return HttpResponse('no product!')
    
    try:
        ad = Address_book.objects.get(userid=cuid,addr_type='def')
    except Address_book.DoesNotExist:
        ad = ''
    res = render_to_response('mall/product.html',{'head': userinfo.get('headimgurl'),'nickname': userinfo.get('nickname','').encode('utf-8'),'islogin':islogin,
                                                  'pinfo':pinfo,'pset':pset,'pdtl':pdtl,'addr':ad})
    
    res.set_cookie('uid', userinfo.get('openid',''))
    res.set_cookie('nickname', userinfo.get('nickname',''))
    res.set_cookie('head', userinfo.get('headimgurl',''))
    return res

def pay(request):
    set_id = request.COOKIES.get('set_id')
    uid = request.COOKIES.get('uid')
    try:
        addr = Address_book.objects.get(userid=uid,addr_type='def')
    except Address_book.DoesNotExist:
        addr = ''
    try:
        pset = Product_sets.objects.get(set_id=set_id)
    except Product_sets.DoesNotExist:
        return HttpResponse('bad order!')
    pro = Product_info.objects.get(product_id=pset.product_id)
    return render_to_response('mall/pay.html',{'addr':addr,'pset':pset,'pro':pro})

def get_prepay_id(request):
    
    def make_sign(appid,body,mch_id,nonce_str,notify_url,openid,out_trade_no,spbill_create_ip,total_fee):
        tmp = """appid=%s&body=%s&mch_id=%s&nonce_str=%s&notify_url=%s&openid=%s&out_trade_no=%s&spbill_create_ip=%s&total_fee=%s&trade_type=JSAPI"""\
            % (appid,body,mch_id,nonce_str,notify_url,openid,out_trade_no,spbill_create_ip,total_fee)
            
        tmp2 = tmp + "&key=yujiahao521realtoraccessokokokok"
        m1 = hashlib.md5()
        m1.update(tmp2)
        return m1.hexdigest().upper()

    openid = request.POST.get('openid','')
    total_fee = request.POST.get('total_fee','1')
    appid = 'wxe530c431696402d0'
    body = '摩尔学院-大数据'
    mch_id = '1491105952'
    nonce_str = 'yujiahao'
    notify_url = 'http://www.realtoraccess.com/mall/wechatcall/'
    openid = openid
    out_trade_no = time.strftime("%Y%m%d%H%M%S", time.localtime(int(time.time())))
    spbill_create_ip = '120.77.50.193'
    total_fee = '1'
    
    para = """
        <xml>
           <appid>%s</appid>
           <body>%s</body>
           <mch_id>%s</mch_id>
           <nonce_str>%s</nonce_str>
           <notify_url>%s</notify_url>
           <openid>%s</openid>
           <out_trade_no>%s</out_trade_no>
           <spbill_create_ip>%s</spbill_create_ip>
           <total_fee>%s</total_fee>
           <trade_type>JSAPI</trade_type>
           <sign>%s</sign>
        </xml>
    """ % (appid,body,mch_id,nonce_str,notify_url,openid,out_trade_no,spbill_create_ip,total_fee,
           make_sign(appid,body,mch_id,nonce_str,notify_url,openid,out_trade_no,spbill_create_ip,total_fee))
    res = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder',data = para.encode('utf-8'))
    
    DOMTree = xml.dom.minidom.parseString(res.content)
    collection = DOMTree.documentElement
    return HttpResponse(collection.getElementsByTagName('prepay_id')[0].firstChild.data)

def get_wechat_sign(request):
    timestamp = request.GET.get('timestamp')
    pid = request.GET.get('pid')
    tmp = """appId=wxe530c431696402d0&nonceStr=yujiahao&package=%s&signType=MD5&timeStamp=%s""" % (pid,timestamp)
    tmp2 = tmp + "&key=yujiahao521realtoraccessokokokok"
    m1 = hashlib.md5()
    m1.update(tmp2)
    return HttpResponse(m1.hexdigest().upper())

def notify_url_wechat(request):
    print request.body
    
    okxml = """
        <xml>
          <return_code><![CDATA[SUCCESS]]></return_code>
          <return_msg><![CDATA[OK]]></return_msg>
        </xml>
    """
    return HttpResponse(okxml)
    
def add_address(request):
    uid = request.POST.get('uid')
    recvname = request.POST.get('recvname')
    recvtel = request.POST.get('recvtel')
    addr = request.POST.get('addr')
    ad = Address_book(userid=uid,recvname=recvname,recvtel=recvtel,addr=addr,addr_type='def',addrid=uuid.uuid1())
    ad.save()
    ads = Address_book.objects.filter(Q(userid=uid),~Q(addrid=ad.addrid))
    for a in ads:
        a.addr_type = 'backup'
        a.save()
    return HttpResponse(ad.addrid)
