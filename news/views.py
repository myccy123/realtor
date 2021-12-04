# -*- coding:utf-8 -*-
from models import *
from app.models import Access_hitory
from django.http.response import HttpResponse,HttpResponseNotFound
from django.shortcuts import render_to_response
from myweb.itools import *
import math
from app.models import Advertisement, Sharesite, Userimage

def get_rcmd_news(request):
    atcs = Article_info.objects.all().order_by('-datadate')[:3]
    alist = []
    for atc in atcs:
        tmp = {}
        tmp['aid'] = atc.id
        tmp['title'] = atc.title
        tmp['date'] = atc.publishdate
        cont = Article_content.objects.filter(articleid=atc.articleid,ptype='img').order_by('pid')
        for c in cont:
            tmp['img'] = c.img.img.url
            break
        if not tmp.get('img'):
            tmp['img'] = 'http://' + request.META['HTTP_HOST'] + '/static/news/img/defad.png'
        alist.append(tmp)
    r = HttpResponse(json.dumps(alist,indent = 2,ensure_ascii=False))
    r["Access-Control-Allow-Origin"] = "*"
    return r    
    
def news_list(request):
    acate = request.GET.get('cate','global')
    page = int(request.GET.get('page','1')) * 10
    atcs = Article_info.objects.filter(articlecate=acate).order_by('-publishdate')[page-10:page]
    lastpage = int(math.ceil(Article_info.objects.filter(articletype=acate).count()/10.0))
    alist = []
    for atc in atcs:
        tmp = {}
        tmp['aid'] = atc.id
        tmp['title'] = atc.title
        tmp['date'] = atc.publishdate
        tmp['pro'] = atc.instr
        if hasattr(atc.img, 'url'):
            tmp['img'] = atc.img.url
        else:
            cont = Article_content.objects.filter(articleid=atc.articleid).order_by('pid')
            if not cont:
                continue
            for c in cont:
                if tmp.get('img'):
                    break
                if c.ptype == 'img':
                    if not hasattr(c.img, 'img'):
                        tmp['img'] = c.pimg.url
                    else:
                        tmp['img'] = c.img.img.url
            if not tmp.get('img'):
                tmp['img'] = 'http://' + request.META['HTTP_HOST'] + '/static/news/img/defad.png'
        alist.append(tmp)
    rcmds = Article_info.objects.filter(src='mp').order_by('-look')[:10]
    rcmd = []
    for r in rcmds:
        tmp = {}
        tmp['title'] = r.title
        tmp['look'] = r.look
        tmp['id'] = r.id
        tmp['cate'] = r.articlecate
        tmp['articletype'] = get_des('t99_articletype', r.articlecate)
        rcmd.append(tmp)
    ads = Advertisement.objects.filter(adtype__in=('atc1','atc2'))
    ad = {}
    ad['atc2'] = []
    for a in ads:
        if a.adtype == 'atc1':
            ad['atc1'] = {'img':a.img.url,'url':a.url}
        elif a.adtype == 'atc2':
            ad['atc2'].append({'img':a.img.url,'url':a.url})
    his = Access_hitory(addr=request.META['REMOTE_ADDR'],actiontype='query',htmltype='newslist',agent=request.META['HTTP_USER_AGENT']
                        ,referer=request.META.get('HTTP_REFERER','url'))
    his.save()
    res = render_to_response('news/newslist.html',{'alist':alist,'atype':acate,
                                'lastpage':lastpage,'rcmd':rcmd,'ad':ad})
    res['X-Frame-Options'] = 'ALLOWALL'
    return res

def get_share_cnt(request):
    articleid = request.GET.get('articleid','')
    if articleid == '':
        ss = Sharesite.objects.filter(sharetype='article')
    else:
        ss = Sharesite.objects.filter(sharetype='article',dataid=articleid)
    res = {}
    for s in ss:
        if not res.get(s.userid):
            res[s.userid] = {}
            res[s.userid]['userid'] = s.userid
            res[s.userid]['cnt'] = 1
            res[s.userid]['img'] = Userimage.objects.get(userid=s.userid,imgtype='ad').img.url
        else:
            res[s.userid]['cnt'] += 1
    sortlist = []
    for userid in res:
        if len(sortlist) == 0:
            sortlist.append(res[userid])
        else:
            for i in range(len(sortlist)):
                if res[userid]['cnt'] >= sortlist[i]['cnt']:
                    sortlist.insert(i,res[userid])
                    break
    return HttpResponse(json.dumps(sortlist,indent = 2,ensure_ascii=False))

def news_page(request,lid):
    try:
        ai = Article_info.objects.get(id=lid)
        ai.look += 1
        ai.save()
    except Article_info.DoesNotExist:
        return HttpResponseNotFound()
    ainfo = {}
    ainfo['articleid'] = ai.articleid
    ainfo['title'] = ai.title
    ainfo['atype'] = ai.articlecate
    ainfo['pdate'] = ai.publishdate
    ainfo['author'] = ai.author
    ainfo['authorurl'] = ai.authorurl
    
    acont = []
    ac = Article_content.objects.filter(articleid=ai.articleid).order_by('pid')
    if not ac:
        return HttpResponseNotFound()
    for a in ac:
        tmp = {}
        tmp['ptype'] = a.ptype
        tmp['pstyle'] = a.pstyle
        tmp['p'] = a.p
        tmp['img'] = a.img.img.url if a.img <> None else a.pimg.url if hasattr(a.pimg, 'url') else ''
        acont.append(tmp)
    
    rcmds = Article_info.objects.filter(src='mp').order_by('-look')[:10]
    rcmd = []
    for r in rcmds:
        tmp = {}
        tmp['title'] = r.title
        tmp['articletype'] = r.articlecate
        tmp['look'] = r.look
        tmp['id'] = r.id
        tmp['cate'] = r.articlecate
        tmp['articletype'] = get_des('t99_articletype', r.articlecate)
        rcmd.append(tmp)
    ads = Advertisement.objects.filter(adtype__in=('atc1','atc2'))
    ad = {}
    ad['atc2'] = []
    for a in ads:
        if a.adtype == 'atc1':
            ad['atc1'] = {'img':a.img.url,'url':a.url}
        elif a.adtype == 'atc2':
            ad['atc2'].append({'img':a.img.url,'url':a.url})
    his = Access_hitory(addr=request.META['REMOTE_ADDR'],actiontype='query',htmltype='newspage',agent=request.META['HTTP_USER_AGENT']
                        ,referer=request.META.get('HTTP_REFERER','url'),htmlid=lid,userid=ai.articletype)
    his.save()
    return render_to_response('news/newspage.html',{'ainfo':ainfo,'acont':acont,'rcmd':rcmd,'ad':ad})

