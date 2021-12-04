# -*- coding:utf-8 -*-
import json
import MySQLdb
import time
import xlrd
import pyodbc
import urllib  
import urllib2
import sys
reload(sys)
from django.http.response import HttpResponse,HttpResponseRedirect
from django.core.files.base import ContentFile
from datetime import date,datetime

class JsnEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, bytearray):
            return ''
        else:
            return json.JSONEncoder.default(self, obj)
        
conn= MySQLdb.connect(
        host='123.57.184.16',
        port = 3306,
        user='root',
        passwd='Ikingcity2016+mysql',
        db ='yitong',
        charset='utf8'
        )
cur = conn.cursor()

sql="select  * from yitong.report_url where   flag= 2"
report_sql=cur.execute(sql)
info_url=cur.fetchmany(report_sql)
for ii in info_url:
    json_file_name=ii[1]
    url=ii[0]
    table_name=ii[10]
    sql_detail="SELECT * FROM  visio_pie.%s  order by name" %table_name
    bb={}
    bb["lyunit"]=""  if ii[5] ==None else ii[5]  
    bb["color"]= "#fff" 
    bb["subtext"] =""  if ii[3] ==None else ii[3]
    bb["title"]= ""  if ii[2] ==None else ii[2] 
    bb["backgroundColor"]="#1b1b1b"  
    report_series=cur.execute(sql_detail)
    info_series=cur.fetchmany(report_series)
    series=[]
    yname=[]
    for  ii in  info_series:
        cc={}
        cc["name"]=ii[0]
        cc["value"]=float(ii[1])
        yname.append(ii[0])
        
        series.append(cc) 
    bb["data"]=series   
    bb["yname"]=yname 
    
    result= json.dumps(bb,indent = 5,ensure_ascii=False,cls=JsnEncoder).encode('utf8') 
    with open(json_file_name, 'w') as f:
        f.write(result)


cur.close()
conn.commit()
conn.close()  
