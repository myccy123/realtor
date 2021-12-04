# -*- coding:utf-8 -*-
import requests
import json


def get_token():
    params = {}
    params['grant_type'] = 'client_credential'
    params['appid'] = 'wxcd1c7e6e724cc101'
    params['secret'] = 'd680d15c670343e17a0bf20dffaf8eeb'
    res = requests.get('https://api.weixin.qq.com/cgi-bin/token',params=params)
    return res.json()['access_token']

def get_token2():
    params = {}
    params['grant_type'] = 'client_credential'
    params['appid'] = 'wxe530c431696402d0'
    params['secret'] = 'b8325c44d50e42eb8410f63333d52b50'
    res = requests.get('https://api.weixin.qq.com/cgi-bin/token',params=params)
    return res.json()['access_token']

def get_token_yvr():
    params = {}
    params['grant_type'] = 'client_credential'
    params['appid'] = 'wx86b375b39cf69443'
    params['secret'] = 'b725f72e9a8f16046aadde6fdfb76fa2'
    res = requests.get('https://api.weixin.qq.com/cgi-bin/token',params=params)
    return res.json()['access_token']


def get_jsapi_ticket():
    token = get_token()
    res = requests.get('https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % token)
    return res.json()['ticket']

def get_taginfo():
    params = {'access_token':get_token()}
    res = requests.get('https://api.weixin.qq.com/cgi-bin/tags/get',params=params)
    print json.dumps(res.json(),indent = 2,ensure_ascii=False)

def send_msg():
    data = """{
       "filter":{
          "is_to_all":false,
          "tag_id":102
       },
       "text":{
          "content":"于家浩的测试信息"
       },
        "msgtype":"text"
    }"""
    token = get_token()
    res = requests.post('https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token=%s' % token,data=data)
    print res.json()

def send_mpnews(media_id):
    data = """{
       "filter":{
          "is_to_all":false,
          "tag_id":102
       },
       "mpnews":{
          "media_id":"%s"
       },
        "msgtype":"mpnews"
    }""" % media_id
    token = get_token()
    res = requests.post('https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token=%s' % token,data=data)
    return res.json()

def upload_img():
    params = {}
    params['access_token'] = get_token()
    files = {'media':open(r'C:\Users\Administrator\Downloads\FireShot\r2177295_m.png','rb')}
    res = requests.post('https://api.weixin.qq.com/cgi-bin/media/uploadimg',params=params,files=files)
    return res.json()#['url']

def upload_material(imgpath):
    params = {}
    params['access_token'] = get_token()
    params['type'] = 'thumb'
    files = {'media':open(imgpath,'rb')}
    res = requests.post('https://api.weixin.qq.com/cgi-bin/material/add_material',params=params,files=files)
    return res.json()['media_id'].encode('utf8')

def upload_news(data):
    token = get_token()
    res = requests.post('https://api.weixin.qq.com/cgi-bin/material/add_news?access_token=%s' \
                        % token,data=data.encode('utf-8'))
    return res.json()['media_id']


