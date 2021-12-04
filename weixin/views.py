# -*- coding:utf-8 -*-
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from wetools import get_jsapi_ticket
import hashlib


def dev_auth(request):
    res = request.GET.get('echostr')
    return HttpResponse(res)

def get_signature(request):
    timestamp = request.GET.get('timestamp')[0:10]
    url = request.GET.get('url')
    noncestr = 'realter'
    jsapi_ticket = get_jsapi_ticket()
    str1 = "jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s" \
            % (jsapi_ticket,noncestr,timestamp,url)
    return HttpResponse(hashlib.sha1(str1).hexdigest())

def get_secure_url(request):
    return render_to_response('MP_verify_eVgil9IPg5X9lWOQ.txt')
