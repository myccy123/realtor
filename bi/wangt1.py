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

conn= MySQLdb.connect(
        host='123.57.184.16',
        port = 3306,
        user='root',
        passwd='Ikingcity2016+mysql',
        db ='yitong',
        charset='utf8'
        )
cur = conn.cursor()

sql="select  * from yitong.report_url"
report_sql=cur.execute(sql)
info_url=cur.fetchmany(report_sql)
for ii in info_url:
    json_file_name=ii[1]
    url=ii[0]    
    sql_detail="SELECT  yAxisIndex,chart_type,echart_columns,scaler,computation_rule,tablename FROM  yitong.report_SQL  where URL=\"%s\"  and xAxis_or_yAxis=\"y\"  order by scaler" %url
    sql_url="SELECT * FROM yitong.report_url where URL=\"%s\"" %url
    bb={}
    report_url=cur.execute(sql_url)
    info=cur.fetchmany(report_url)
    for ii in info:
#        json_file_name=ii[1]
        bb["lyunit"]=""  if ii[5] ==None else ii[5]  
        bb["ryunit"]= "" if ii[6] ==None else ii[6]
        bb["subtext"] =""  if ii[3] ==None else ii[3]
        bb["title"]= ""  if ii[2] ==None else ii[2] 
        bb["xunit"]= "" if ii[4] ==None else ii[4] 
        bb["lyname"]= ""  if ii[7] ==None else ii[7]
        bb["formatter"] =""  if ii[9] ==None else ii[9]
        bb["ryname"]=""  if ii[8] ==None else ii[8]
    report_series=cur.execute(sql_detail)
    info_series=cur.fetchmany(report_series)
    sql_detail_x="SELECT  echart_columns  FROM  yitong.report_SQL  where URL=\"%s\"  and xAxis_or_yAxis=\"x\"  order by scaler" %url
    report_series_x=cur.execute(sql_detail_x)
    info_series_x=cur.fetchmany(report_series_x)
    for  ii in  info_series_x:
        x=ii[0]
    series=[]
    yname=[]
    for  ii in  info_series:
        cc={}
        cc["yAxisIndex"]=ii[0]
        cc["type"]=ii[1]
        cc["name"]=ii[2]
        cc["unit"]=bb["lyunit"] if ii[0]=="0" else bb["ryunit"]
        yname.append(ii[2])
        sql_a='select %s,%s(%s)  from %s  group by %s   order by %s' %(x,ii[4],ii[2],ii[5],x,x)
        report_data=cur.execute(sql_a)
        info_data=cur.fetchmany(report_data)
        data=[]
        for ii in info_data:
            data.append(float(ii[1]))
        
        cc["data"]=data
        
        series.append(cc)
    report_sql_x=cur.execute(sql_a)
    info_sql_x=cur.fetchmany(report_sql_x) 
    xAxis=[]  
    for ii in info_sql_x:
        xAxis.append(ii[0])
     
    bb["xAxis"]=xAxis   
    bb["series"]=series   
    bb["yname"]=yname 
    result= json.dumps(bb,indent = 5,ensure_ascii=False).encode('utf8') 
    with open(json_file_name, 'w') as f:
        f.write(result)
#    print result
#    url ='bbb.txt'
#    url ='http://www.ikingcity.cn:8000/data/chartdata/yujh_7PKIJkg.txt'  
#    json_url='%s' %json_file_name
#    print json_file_name
#    data = urllib.urlencode(bb) 
#    print data

#     req = urllib2.Request(json_file_name, result) 
#     response = urllib2.urlopen(req) 
#     the_page = response.read() 
#     print  the_page


cur.close()
conn.commit()
conn.close()  
