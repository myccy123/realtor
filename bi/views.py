# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http.response import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from bi.models import *
from bi.forms import *
from biutil import MySql
import json
import uuid
import re
import base64

def decode_base64(data):
    if data =='' or data == None:
        return ''
    data = data.split(',')[1]
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return base64.decodestring(data)

def where_rule_info(selpostdata):
    whererule=''
    for i in range(10):
        selclassdata = selpostdata.get('selclassdata'+str(i),'').strip()
        selclasscompu = selpostdata.get('selclasscompu'+str(i),'').strip()
        selclassva = selpostdata.get('selclassval'+str(i),'').strip()
        if selclassdata <> '':
            if selclasscompu=='eq':
                whererule += " and `%s` = '%s' " % (selclassdata,selclassva)
            elif  selclasscompu=='noeq':   
                whererule += " and `%s` <> '%s' " % (selclassdata,selclassva)
            elif selclasscompu=='gt':
                whererule +=' and `'+selclassdata +'` > ' +selclassva
            elif selclasscompu == 'lt':
                whererule +=' and `' + selclassdata +'` < ' +selclassva
            elif selclasscompu =='gteq':
                whererule +=' and `' + selclassdata +'` >= '+selclassva
            elif selclasscompu =='lteq':
                whererule +=' and `'+selclassdata +'` <= ' +selclassva
            elif selclasscompu=='blank':
                whererule +=' and `'+selclassdata +'` is null '
            elif selclasscompu=='noblank':
                whererule +=' and `' +selclassdata +'` is not null '   
            elif selclasscompu=='data':
                (bgndt,enddt) = selclassva.split(',')
                bgndt = '1900-01-01 00:00:00' if bgndt == 'undefined' else bgndt
                enddt = '2199-12-31 00:00:00' if enddt == 'undefined' else enddt
                bgndt = bgndt.replace('/',' ').replace(' ','-',2)
                enddt = enddt.replace('/',' ').replace(' ','-',2)
                whererule += " and `%s` between '%s' and '%s' " % (selclassdata,bgndt,enddt)
    return whererule 

def index(request):
    return render_to_response('bi/index.html')

def login(request):
    return render_to_response('bi/login.html')

def tologout(request):
    logout(request)
    return HttpResponse('0')

def has_login(request):
    if request.user.is_authenticated():
        return HttpResponse('1')
    else:
        return HttpResponse('0')

@login_required(login_url='/bi/login/')
def addsource(request):
    if request.user.is_authenticated():
        return render_to_response('bi/mathData.html')
    else:
        return HttpResponse('please login...')

@login_required(login_url='/bi/login/')
def addexcel(request):
    if request.user.is_authenticated():
        userid = request.COOKIES['id']
        s = Source.objects.filter(sourcefrom = userid)
        return render_to_response('bi/addExcel.html',{'sourcenames' : s})
    else:
        return HttpResponse('please login...')

def upload_excel(request):
    sourcename = request.POST.get('sourcename')
    perm = request.POST.get('perm')
    xls = request.FILES.get('excel')
    xls.name = 'abc'
    src = Source(sourceid=uuid.uuid1(),sourcename=sourcename,sourcepermi=perm,
                 sourcefrom=request.COOKIES['id'],sourcetype='excel',realtime='0')
    src.save()
    src.datais = 't'+str(src.id)
    src.save()
    sf = Source_file(sourceid=src.sourceid,filetype='excel',file=xls)
    sf.save()
    print sf.file.path
    print sf.file.name
    MySql.create_excel_tab(sf.file.path,src.datais)
    return HttpResponseRedirect(reverse('bi:excel'))

@login_required(login_url='/bi/login/')
def addmysql(request):
    if request.user.is_authenticated():
        userid = request.COOKIES['id']
        s = Source.objects.filter(sourcefrom = userid)
        return render_to_response('bi/matchMysql.html',{'sourcenames' : s})
    else:
        return HttpResponse('please login...')

@login_required(login_url='/bi/login/')
def addchart(request):
    if request.user.is_authenticated():
        return render_to_response('bi/detail.html')
    else:
        return HttpResponse('please login...')

def getperm(request):
    if request.method == 'GET':
        userid = request.COOKIES['id']
        perm = {}
        perm['all'] = '所有人'
        perm['self'] = '仅自己'
        res = json.dumps(perm,indent = 2,ensure_ascii=False)
        return HttpResponse(res)
    else:
        return HttpResponse('please get')
        
def confconn(request):
    form = Mysqlconn(request.POST)
    if form.is_valid():
        mysqle_ip = form.cleaned_data['mysqle_ip']
        mysqle_user = form.cleaned_data['mysqle_user']
        mysqle_psw = form.cleaned_data['mysqle_psw']
        mysqle_port = form.cleaned_data['mysqle_port']
        dbtree = MySql.read_dbtree(mysqle_ip, mysqle_user, mysqle_psw, mysqle_port)
        res = json.dumps(dbtree,indent = 2,ensure_ascii=False)
        return HttpResponse(res)
    else:
        err = ''
        for e in form.errors:
            err = err+e+'->'+form.errors[e]+'|||'
        return HttpResponse(err)

def conftab(request):
    form = Mysqltab(request.POST)
    if form.is_valid():
        userid = request.COOKIES['id']
        mysqle_dataSource = form.cleaned_data['mysqle_dataSource']
        mysqle_permiss = form.cleaned_data['mysqle_permiss']
        mysqle_ip = form.cleaned_data['mysqle_ip']
        mysqle_user = form.cleaned_data['mysqle_user']
        mysqle_psw = form.cleaned_data['mysqle_psw']
        mysqle_port = form.cleaned_data['mysqle_port']
        conntype = form.cleaned_data['checked']
        db = form.cleaned_data['db']
        tab = form.cleaned_data['tab']
        src = Source(sourceid = uuid.uuid1(),sourcename=mysqle_dataSource,
                     sourcetype = 'mysql',datais = tab,sourcepermi = mysqle_permiss,sourcefrom = userid,
                     isenable = '1',sourceip=mysqle_ip,sourceuser=mysqle_user,sourcepasswd=mysqle_psw,
                     sourceport=mysqle_port,sourcedb=db,realtime='1')
        src.save()
        return HttpResponse('ok')
    else:
        err = ''
        for e in form.errors:
            err = err+e+'->'+form.errors[e]+'|||'
        return HttpResponse(err)   

def getsourcename(request):
    if request.method == 'GET':
        userid = request.COOKIES['id']
        keyword = request.GET.get('keyword')
        if keyword:
            src = Source.objects.filter(sourcefrom = userid,sourcename__icontains=keyword)
        else:
            src = Source.objects.filter(sourcefrom = userid)
        arr = []
        for s in src:
            jsn = {}
            jsn['sourceid'] = s.sourceid
            jsn['sourcename'] = s.sourcename
            jsn['sourcetype'] = 'M' if s.sourcetype == 'mysql' else 'E'
            arr.append(jsn)
        res = json.dumps(arr,indent = 2,ensure_ascii=False)
        return HttpResponse(res)
    else:
        return HttpResponse('please login!')

def getsourceinfo(request):
    form = Sourceid(request.POST)
    if form.is_valid():
        sourceid = form.cleaned_data['sourceid']
        src = Source.objects.get(sourceid = sourceid)
        jsn = MySql.read_tab(src.datais,src.sourceip,src.sourceuser,src.sourcepasswd,src.sourceport,src.sourcedb)
        jsn['sourceid'] = sourceid
        jsn['srcname'] = src.sourcename
        jsn['srcimg'] = '#'
        jsn['srcowner'] = ''
        jsn['srcownerhead'] = ''
        jsn['realtime'] = src.realtime
        a = json.dumps(jsn,indent = 2,ensure_ascii=False)
        res = HttpResponse(a)
        res.set_cookie('srcid', sourceid)
        return res
    else:
        err = ''
        for e in form.errors:
            err = err+e+'->'+form.errors[e]+'|||'
        return HttpResponse(err)   

def getsourceinfo2(request):
    sourceid = request.COOKIES['srcid']
    src = Source.objects.get(sourceid = sourceid)
    jsn = MySql.read_tab(src.datais,src.sourceip,src.sourceuser,src.sourcepasswd,src.sourceport,src.sourcedb)
    jsn['sourceid'] = sourceid
    jsn['realtime'] = src.realtime
    return HttpResponse(json.dumps(jsn,indent = 2,ensure_ascii=False))

def read_tab(request):
    db = request.GET.get('db')
    tabs = MySql.read_tab_ofdb(db)
    return HttpResponse(json.dumps(tabs,indent = 2,ensure_ascii=False))

def read_datatype(request):
    keyword = request.GET.get('keyword')
    res = []
    if keyword:
        dt = User_data.objects.filter(datatype__icontains=keyword).values('datatype').distinct()
    else:
        dt = User_data.objects.all().values('datatype').distinct()
    for t in dt:
        res.append(t['datatype'])
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))



def make_pie_data(request):
    print json.dumps(request.POST,indent = 2,ensure_ascii=False)
    srcid = request.COOKIES['srcid']
    userid = request.COOKIES['id']
    ctype = request.POST.get('ctype')
    src = Source.objects.get(sourceid = srcid)
    dbtab = (src.sourcedb + '.') if src.realtime == '1' else ''
    dbtab += '`%s`' % src.datais   
    x = request.POST.get('selx') 
    title = request.POST.get('maintitle')
    subtitle = request.POST.get('childtitle')
    uint = request.POST.get('lyuint')
    sv = request.POST.get('saveV')
    datatype = request.POST.get('datatype','')
    img = decode_base64(request.POST.get('charticon'))
    rttype = request.POST.get('rttype','')
    theme = request.POST.get('theme','')
    sortcol = request.POST.get('tabHightSourceSelect','')
    sortas = request.POST.get('tabHightSourceSort','asc')
    if sortas == '1':
        sortas = 'asc'
    elif sortas == '0':
        sortas = 'desc'
    selpostdata = request.POST
    y = []
    s = []
    for i in range(10):
        y1 = request.POST.get('selyF'+str(i),'')
        s1 = request.POST.get('selyS'+str(i),'')
        if y1 == '' or s1 == '':
            break
        else:
            y.append(y1)
            s.append(s1)
    if ctype <> None and len(y) > 0  and len(y) > 0:
        where_rule1=' where 1=1 '+ where_rule_info(selpostdata)
        data = []        
        if sortcol in y:
            sortcol = '%s(`%s`)' % (s[y.index(sortcol)],sortcol)
        if x <> '':       
            sql = 'select ' + '`%s`' % x
            sql += ',%s(`%s`)' % (s[0],y[0])
            sql += ' from %s  %s  group by `%s` order by %s %s' % (dbtab,where_rule1,x,
                    '`%s`' % x if x == '' else x,'desc' if src.realtime == '1' else sortas)
            print sql
            yname = []
            data = []
            for row in MySql.sel_table(sql,src.sourceip,src.sourceuser,src.sourcepasswd,src.sourceport):
                jsn = {}
                jsn['name'] = row[0]
                jsn['value'] = row[1]
                jsn['seriesname'] = y[0]
                yname.append(row[0])
                data.append(jsn)
        elif x == '':
            sql='select '
            for i in range(len(y)):
                if i==0 :
                    sql += '%s(`%s`)' % (s[i],y[i])
                elif i>0:
                    sql += ',%s(`%s`)' % (s[i],y[i])
            sql += ' from %s  %s  ' % (dbtab,where_rule1)    
            yname =[]
            data =[]
            for row in MySql.sel_table(sql,src.sourceip,src.sourceuser,src.sourcepasswd,src.sourceport):
                for i in range(len(y)):
                    jsn = {}
                    jsn['name'] =y[i]
                    jsn['value']=row[i]
                    jsn['seriesname'] = '总计'.encode('utf-8')
                    yname.append(y[i])
                    data.append(jsn)
        cont = {}
        cont['title'] = title
        cont['subtext'] = subtitle
        cont['backgroundColor'] = '#1b1b1b'
        cont['color'] = '#fff'
        cont['lyunit'] = uint
        cont['yname'] = yname
        cont['data'] = data
        a = json.dumps(cont,indent = 2,ensure_ascii=False).encode('utf8')
        myfile = ContentFile(a)
        if sv == '1':
            ud = User_data(chartid = uuid.uuid1(),charttype = ctype,userid = userid
                      ,visualof = 'all',chartname = request.POST.get('maintitle')
                      ,datatype=datatype,srcid=srcid,rttype=rttype,theme=theme)
            ud.save()
            ud.dataicon.save('icon.png',ContentFile(img))
            js = {}
            js['done'] = '1'
            js['ctype'] = ctype
            js['jsn'] = ''
            Json_file_name1=ud.data.name
            if x <> '':
                jsncolumnsx = Echarts_Json_columns(chartid=ud.chartid,tablename=dbtab,echart_columns=x,xAxis_or_yAxis='x',scaler=0,where_rule=where_rule1) 
                jsncolumnsx.save()
                jsncolumnsy=Echarts_Json_columns(chartid=ud.chartid,tablename=dbtab,echart_columns=y[0],computation_rule=s[0],chart_type='NULL',xAxis_or_yAxis='y',yAxisIndex='NULL',scaler=1,where_rule=where_rule1)
                jsncolumnsy.save() 
                jsoninfo=Echarts_Json_info(chartid=ud.chartid,Json_file_name=Json_file_name1,title=cont['title'],subtext=cont['subtext'],xunit='NULL',lyunit=cont['lyunit'] ,ryunit='NULL',lyname='NULL' ,ryname='NULL' ,formatter='NULL',report_sql=sql,flag = 2 )
                jsoninfo.save()
            elif x == '':
                jsoninfo=Echarts_Json_info(chartid=ud.chartid,Json_file_name=Json_file_name1,title=cont['title'],subtext=cont['subtext'],xunit='NULL',lyunit=cont['lyunit'] ,ryunit='NULL',lyname='NULL' ,ryname='NULL' ,formatter='NULL',report_sql=sql,flag = 21 )
                jsoninfo.save()
                for i in range(len(y)):
                    jsncolumnsy=Echarts_Json_columns(chartid=ud.chartid,tablename=dbtab,echart_columns=y[i],computation_rule=s[i],chart_type='NULL',xAxis_or_yAxis='y',yAxisIndex='NULL',scaler=i,where_rule=where_rule1)
                    jsncolumnsy.save() 
            return HttpResponse(json.dumps(js,indent = 2,ensure_ascii=False))
        else:
            if rttype == 'rtline':
                ud = Tmpdata(sqls=sql,rttype=rttype,jsn=a)
                ud.save()
                js = {}
                js['tmpid'] = ud.id
                js['ctype'] = ctype
                js['srcid'] = srcid
                js['jsn'] = ''
                js['done'] = '0'
                js['theme'] = theme
                return HttpResponse(json.dumps(js,indent = 2,ensure_ascii=False))
            else:
                ud = Tmpdata()
                ud.save()
                ud.data.save(userid+'.txt',myfile)  
                js = {}
                js['tmpid'] = ud.id
                js['ctype'] = ctype
                js['jsn'] = ud.data.url
                js['srcid'] = srcid
                js['done'] = '0'
                js['theme'] = theme
                return HttpResponse(json.dumps(js,indent = 2,ensure_ascii=False))
    
    else:
        return HttpResponse('nothing')


def make_map_data(request):
    userid = request.COOKIES['id']
    ctype = request.POST.get('ctype')
    dbname = request.POST.get('db')
    tabname = request.POST.get('selyF0')
    title = request.POST.get('maintitle')
    subtitle = request.POST.get('childtitle')
    sv = request.POST.get('saveV')
    datatype = request.POST.get('datatype','')
    theme = request.POST.get('theme','')
    img = decode_base64(request.POST.get('charticon'))
    if datatype.strip() == '':
        datatype = '未分类'
    sql1 = 'select place,val,lng,lat,valname from %s.%s' % (dbname,tabname)
    sql2 = 'select place,val from %s.%s where val < minval or val > maxval' % (dbname,tabname)
    sql3 = 'select max(val) from %s.%s' % (dbname,tabname)
    series = []
    series1 = []
    seriesname = {}
    dataname = ''
    dataRangemax = float(MySql.sel_table(sql3).next()[0])
    for row in MySql.sel_table(sql1):
        jsn = {}
        jsn['name'] = row[0]
        jsn['value'] = float(row[1])
        series.append(jsn)
        seriesname[row[0]] = [float(row[2]),float(row[3])]
        dataname = row[4] if row[4] <> None else "66" 
    for row in MySql.sel_table(sql2):
        jsn = {}
        jsn['name'] = row[0]
        jsn['value'] = float(row[1])
        series1.append(jsn)
    cont = {}
    cont['title'] = title
    cont['subtext'] = subtitle
    dn = []
    dn.append(dataname)
    cont['dataname'] = dn
    cont['dataRangemax'] = dataRangemax
    cont['series'] = series
    cont['series1'] = series1
    cont['seriesname'] = seriesname
    a = json.dumps(cont,indent = 2,ensure_ascii=False).encode('utf8')
    myfile = ContentFile(a)
    ud = ''
    js = {}
    if sv == '1':
        ud = User_data(chartid = uuid.uuid1(),charttype = ctype,userid = userid
                    ,visualof = 'all',chartname = title,datatype=datatype,theme=theme)
        js['done'] = '1'
        ud.dataicon.save('icon.png',ContentFile(img))
    else:
        ud = Tmpdata()
        js['done'] = '0'
        js['theme'] = theme
    ud.save()
    ud.data.save(userid+'.txt',myfile)
    js['ctype'] = ctype
    js['jsn'] = ud.data.url
    return HttpResponse(json.dumps(js,indent = 2,ensure_ascii=False))

def make_dashboard_data(request):
    userid = request.COOKIES['id']
    ctype = request.POST.get('ctype')
    dbname = request.POST.get('db')
    tabname = request.POST.get('selyF0')
    title = request.POST.get('maintitle')
    subtitle = request.POST.get('childtitle')
    unit = request.POST.get('lyuint')
    sv = request.POST.get('saveV')
    datatype = request.POST.get('datatype','')
    theme = request.POST.get('theme','')
    img = decode_base64(request.POST.get('charticon'))
    if datatype.strip() == '':
        datatype = '未分类'
    sql = 'select * from %s.%s order by montime desc limit 1' % (dbname,tabname)
    jsn = {}
    for row in MySql.sel_table(sql):
        data = []
        data2 = {}
        data2['value'] = float(row[1])
        data2['name'] = row[7]
        data.append(data2)
        jsn['title'] = title
        jsn['subtext'] = subtitle
        jsn['backgroundColor'] = '#1b1b1b'
        jsn['color'] = '#fff'
        jsn['unit'] = unit
        jsn['colordata1'] = float(row[2])
        jsn['colordata2'] = float(row[3])
        jsn['colordata3'] = float(row[4])
        jsn['data'] = data
    a = json.dumps(jsn,indent = 2,ensure_ascii=False).encode('utf8')
    myfile = ContentFile(a)
    ud = ''
    res = {}
    if sv == '1':
        ud = User_data(chartid = uuid.uuid1(),charttype = ctype,userid = userid
                    ,visualof = 'all',chartname = title,srctab = dbname+'.'+tabname,datatype=datatype,theme=theme)
        res['done'] = '1'
        ud.dataicon.save('icon.png',ContentFile(img))
    else:
        ud = Tmpdata(srctab = dbname+'.'+tabname)
        res['done'] = '0'
        res['theme'] = theme
    ud.save()
    ud.data.save(userid+'.txt',myfile)
    res['url'] = 'http://' + request.META['HTTP_HOST'] + reverse('get:rtchart',args = (str(ud.id),))
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def get_realtime_chart(request,dataid):
    flag = request.GET.get('publish')
    jsn = {}
    if flag == '1':
        d = User_data.objects.get(id = dataid)
        sql = 'select * from %s order by montime desc limit 1' % d.srctab
        newval = MySql.sel_table(sql).next()[1].encode('utf-8')
        cont = d.data.read()
        newcont = re.sub(re.compile('.*value.*'), '     "value": %s' % newval,cont)
#         with open(d.data.path,'w') as f:
#             f.write(newcont)
        chartid = d.chartid
        chartname = d.chartname
        charttype = d.charttype
        data = json.loads(newcont) #d.data.url
        dataicon = ''
        if hasattr(d.dataicon,'url'):
            dataicon = d.dataicon.url
        jsn['chartid'] = chartid
        jsn['ctype'] = charttype
        jsn['data'] = data
        jsn['dataicon'] = dataicon
        jsn['chartname'] = chartname
        return HttpResponse(json.dumps(jsn,indent = 2,ensure_ascii=False))
    else:
        d = Tmpdata.objects.get(id = dataid)
        sql = 'select * from %s order by montime desc limit 1' % d.srctab
        newval = MySql.sel_table(sql).next()[1].encode('utf-8')
        cont = d.data.read()
        newcont = re.sub(re.compile('.*value.*'), '     "value": %s' % newval,cont)
#         with open(d.data.path,'w') as f:
#             f.write(newcont)
        jsn['data'] = json.loads(newcont) #d.data.url
        return HttpResponse(json.dumps(jsn,indent = 2,ensure_ascii=False))


def make_line_data(request):
    
    srcid = request.COOKIES['srcid']
    userid = request.COOKIES['id']
    src = Source.objects.get(sourceid = srcid)
    dbtab = (src.sourcedb + '.') if src.realtime == '1' else ''
    dbtab += '`%s`' % src.datais
    ctype = request.POST.get('ctype')
    x = request.POST.get('selx','')
    legend = request.POST.get('legend','')  
    sv = request.POST.get('saveV')
    datatype = request.POST.get('datatype','')
    datatype = '未分类' if datatype.strip() == '' else datatype
    rttype = request.POST.get('rttype','')
    sortcol = request.POST.get('tabHightSourceSelect','')
    sortas = request.POST.get('tabHightSourceSort','asc')
    theme = request.POST.get('theme','')
    sortas = 'asc' if sortas == '1' else 'desc'
    timewindow = request.POST.get('timewindow','20')
    timewindow = timewindow if timewindow <> '' else '20'
    timewindow = timewindow if int(timewindow) <= 1000 else '1000'
    selpostdata = request.POST
    img = decode_base64(request.POST.get('charticon'))
    y = []
    s = []
    st = []
    yAxisIndex = []
    for i in range(10):
        y1 = request.POST.get('selyF'+str(i),'')
        s1 = request.POST.get('selyS'+str(i),'')
        st1 = request.POST.get('selySt'+str(i))
        yAxisIndex1 = request.POST.get('yAxisIndex'+str(i),'')
        if y1 == '' or s1 == '':
            break
        else:
            y.append(y1)
            s.append(s1)
            st.append(st1)
            yAxisIndex.append(yAxisIndex1)
    
    if ctype <> None and x <> '' and len(y) > 0 and len(s) > 0:
        where_rule1=' where 1=1 '+ where_rule_info(selpostdata)
        data = []
        datalv = []
        series = []
        for l in range(len(y)+1):
            data.append([])
        if sortcol in y:
            sortcol = '%s(`%s`)' % (s[y.index(sortcol)],sortcol)
        sql = 'select ' + '`%s`' % x
        sql += ',%s' % legend if legend <> '' else ''
        for i in range(len(y)):
            sql += ',%s(`%s`)' % (s[i],y[i])
        if legend <> '' :
            sql += ' from %s  %s  group by `%s`,`%s` order by %s %s' % (dbtab,where_rule1,x,legend,
                    '`%s`' % x if sortcol == '' else sortcol,'desc' if rttype == 'rtline' else sortas) 
            for row in MySql.sel_table(sql,src.sourceip,src.sourceuser,src.sourcepasswd,src.sourceport):
                datalv.append(row)
            
            datalegend = {}
            xcols = []
            for row in datalv:
                if not datalegend.get(row[1]):
                    datalegend[row[1]] = []
                if row[0] not in xcols:
                    xcols.append(row[0])
            
            for d in datalegend:
                for i in range(len(xcols)):
                    datalegend[d].append('')
            
            for row in datalv:
                datalegend[row[1]][xcols.index(row[0])] = row[2]
                    
            for l in datalegend:
                srs={} 
                srs['data'] = datalegend[l]
                srs['name'] = l
                srs['type'] = ''
                srs['unit'] = request.POST.get('lyuint','')
                srs['yAxisIndex'] = ''
                series.append(srs)
        else:
            sql += ' from %s  %s  group by `%s` order by %s %s' % (dbtab,where_rule1,x,
                    '`%s`' % x if sortcol == '' else sortcol,'desc' if rttype == 'rtline' else sortas)  
            for row in MySql.sel_table(sql,src.sourceip,src.sourceuser,src.sourcepasswd,src.sourceport):
                for r in range(len(row)):
                    data[r].append(row[r])
            for i in range(len(data)-1):
                srs = {}
                numdata = []
                for n in data[i+1]:
                    numdata.append(float(n))
                srs['data'] = numdata if rttype <> 'rtline' else []
                srs['name'] = y[i]
                srs['type'] = st[i]
                srs['unit'] = request.POST.get('lyuint','') if yAxisIndex[i] == '0' else request.POST.get('ryuint','')
                srs['yAxisIndex'] = yAxisIndex[i]
                series.append(srs)
        print series
        print sql         
        jsn = {}
        jsn['title'] = request.POST.get('maintitle')
        jsn['subtext'] = request.POST.get('childtitle')
        jsn['xunit'] = request.POST.get('xuint','')
        jsn['lyunit'] = request.POST.get('lyuint','')
        jsn['ryunit'] = request.POST.get('ryuint','')
        jsn['formatter'] = ''
        jsn['yname'] = datalegend.keys() if legend <> '' else y
        jsn['xAxis'] = xcols if legend <> '' else data[0] if rttype <> 'rtline' else []
        jsn['lyname'] = ''
        jsn['ryname'] = ''
        jsn['series'] = series
        a = json.dumps(jsn,indent = 5,ensure_ascii=False).encode('utf8')
        myfile = ContentFile(a)
        if sv == '1':
            ud = User_data(chartid = uuid.uuid1(),charttype = ctype,userid = userid
                      ,visualof = 'all',chartname = request.POST.get('maintitle')
                      ,datatype=datatype,srcid=srcid,rttype=rttype,timewindow=timewindow,theme=theme)
            ud.save()
            ud.dataicon.save('icon.png',ContentFile(img))
            udd = Tmpdata(sqls=sql,rttype=rttype,jsn=a,timewindow=timewindow)
            udd.save()
            js = {}
            js['done'] = '1'
            js['ctype'] = ctype
            js['jsn'] = a
            Json_file_name1=ud.data.name
            jsncolumnsx = Echarts_Json_columns(chartid=ud.chartid,tablename=dbtab,echart_columns=x,xAxis_or_yAxis='x',scaler=0,where_rule=where_rule1) 
            jsncolumnsx.save()
            jsoninfo=Echarts_Json_info(chartid=ud.chartid,Json_file_name=Json_file_name1,title=jsn['title'],subtext=jsn['subtext']
                                       ,xunit=jsn['xunit'],lyunit=jsn['lyunit'] ,ryunit=jsn['ryunit'],lyname=jsn['lyname'] ,ryname=jsn['ryname'] 
                                       ,formatter=jsn['formatter'],report_sql=sql,flag = 11 if legend <> '' else 1)
            jsoninfo.save()
            for i in range(len(y)):
                jsncolumnsy=Echarts_Json_columns(chartid=ud.chartid,tablename=dbtab,echart_columns=y[i],computation_rule=s[i],chart_type=st[i],xAxis_or_yAxis='y',yAxisIndex=yAxisIndex[i],scaler=i+2,where_rule=where_rule1)
                jsncolumnsy.save() 
            return HttpResponse(json.dumps(js,indent = 2,ensure_ascii=False))
        else:
            if rttype == 'rtline':
                ud = Tmpdata(sqls=sql,rttype=rttype,jsn=a,timewindow=timewindow)
                ud.save()
                js = {}
                js['tmpid'] = ud.id
                js['ctype'] = ctype
                js['srcid'] = srcid
                js['timewindow'] = int(timewindow)
                js['jsn'] = ''
                js['theme'] = theme
                js['done'] = '0'
                return HttpResponse(json.dumps(js,indent = 2,ensure_ascii=False))
            else:               
                ud = Tmpdata()
                ud.save()
                ud.data.save(userid+'.txt',myfile)
                js = {}
                js['tmpid'] = ud.id
                js['ctype'] = ctype
                js['jsn'] = ud.data.url
                js['theme'] = theme
                js['srcid'] = srcid
                js['done'] = '0'
                return HttpResponse(json.dumps(js,indent = 2,ensure_ascii=False))
    else:
        return HttpResponse('nothing')

def make_thermodynamic_data(request):
    srcid = request.COOKIES['srcid']
    userid = request.COOKIES['id']
    src = Source.objects.get(sourceid = srcid)
    dbtab = (src.sourcedb + '.') if src.realtime == '1' else ''
    dbtab += '`%s`' % src.datais
    title = request.POST.get('maintitle')
    subtitle = request.POST.get('childtitle')
    datatype = request.POST.get('datatype','')
    datatype = '未分类' if datatype.strip() == '' else datatype
    x = request.POST.get('rowmark','')
    y = request.POST.get('colmark','')
    v = request.POST.get('heat_data_source','')
    r = request.POST.get('countmethod','sum')
    theme = request.POST.get('theme','')
    sortcol = request.POST.get('tabHightSourceSelect','')
    sortas = request.POST.get('tabHightSourceSort','asc')
    sv = request.POST.get('saveV')
    ctype = request.POST.get('ctype')
    img = decode_base64(request.POST.get('charticon'))
    selpostdata = request.POST
    where_rule1=' where 1=1 '+ where_rule_info(selpostdata)
    if x <> '' and y <> '' and v <> '':
        sql = 'select ' + '`%s`,`%s`,%s(`%s`) ' % (x,y,r,v)
        sql += ' from %s  %s  group by `%s`,`%s` order by %s %s' % (dbtab,where_rule1,x,y,
                    '`%s`' % x+',`%s`' % y if sortcol == '' else sortcol, sortas)
        print sql
        sql2 = 'select `%s` from %s %s group by `%s` order by `%s`' % (y,dbtab,where_rule1,y,y)
        ys = [row[0] for row in MySql.sel_table(sql2,src.sourceip,src.sourceuser,src.sourcepasswd,src.sourceport)]
        xs = []
        alldata = {}
        resdata = []
        for row in MySql.sel_table(sql,src.sourceip,src.sourceuser,src.sourcepasswd,src.sourceport):
            if not alldata.get(row[0]):
                alldata[row[0]] = {}
            alldata[row[0]][row[1]] = float(row[2])
            
            if row[0] not in xs:
                xs.append(row[0])
        for i in xs:
            for j in ys:
                tmp = []
                tmp.append(ys.index(j))
                tmp.append(xs.index(i))
                tmp.append(alldata.get(i).get(j,''))
                resdata.append(tmp)
        
        jsn = {}
        jsn['title'] = title
        jsn['subtext'] = subtitle
        jsn['series'] = resdata
        jsn['yname'] = ys
        jsn['xAxis'] = xs
        jsn['xunit'] = ''
        myfile = ContentFile(json.dumps(jsn,indent = 2,ensure_ascii=False))
        js = {}
        if sv == '1':
            ud = User_data(chartid = uuid.uuid1(),charttype = ctype,userid = userid
                        ,visualof = 'all',chartname = title,datatype=datatype,theme=theme,srcid=srcid)
            js['done'] = '1'
            ud.dataicon.save('icon.png',ContentFile(img))
            ud.save()
            jsncolumnsx = Echarts_Json_columns(chartid=ud.chartid,tablename=dbtab,echart_columns=x,xAxis_or_yAxis='x',scaler=0,where_rule=where_rule1) 
            jsncolumnsy = Echarts_Json_columns(chartid=ud.chartid,tablename=dbtab,echart_columns=y,xAxis_or_yAxis='y',scaler=1,where_rule=where_rule1) 
            jsncolumnsv = Echarts_Json_columns(chartid=ud.chartid,tablename=dbtab,computation_rule=r,echart_columns=y,xAxis_or_yAxis='v',scaler=2,where_rule=where_rule1) 
            jsncolumnsx.save()
            jsncolumnsy.save()
            jsncolumnsv.save()
            jsoninfo=Echarts_Json_info(chartid=ud.chartid,title=jsn['title'],subtext=jsn['subtext']
                                       ,xunit=jsn['xunit'],report_sql=sql,flag = 3)
            jsoninfo.save()
        else:
            ud = Tmpdata()
            js['done'] = '0'
            js['theme'] = theme
            ud.save()
            ud.data.save(userid+'.txt',myfile)
            js['jsn'] = ud.data.url
        js['ctype'] = ctype
        return HttpResponse(json.dumps(js,indent = 2,ensure_ascii=False))
    else:
        return HttpResponse('nothing')

@login_required(login_url='/bi/login/')
def monitoring(request):
    if request.user.is_authenticated():
        return render_to_response('bi/system.html')
    else:
        return HttpResponse('please login...')

def getchart(request):
    userid = request.COOKIES['id']
    dtype = request.GET.get('datatype')
    dbdata = ''
    if not dtype:
        dbdata = User_data.objects.all().filter(userid = userid)
    else:
        try:
            dbdata = [User_data.objects.get(chartid=dtype)]
        except User_data.DoesNotExist:
            dbdata = User_data.objects.filter(userid = userid,datatype=dtype)
    res = {}
    for d in dbdata:
        res[str(d.datatype)] = []
    for d in dbdata:
        jsn = {}
        dataicon = ''
        if hasattr(d.dataicon,'url'):
            dataicon = d.dataicon.url
        jsn['chartid'] = d.chartid
        jsn['ctype'] = d.charttype
        jsn['data'] = '' #d.data.url
        jsn['dataicon'] = dataicon
        jsn['chartname'] = d.chartname
        jsn['datatype'] = str(d.datatype)
        jsn['srcid'] = d.srcid
        jsn['rttype'] = d.rttype
        jsn['theme'] = d.theme
        jsn['timewindow'] = int(d.timewindow) if d.timewindow <> '' else 0
        if d.srctab <> '':
            jsn['wrapurl'] = 'http://' + request.META['HTTP_HOST'] + reverse('get:rtchart',args = (str(d.id),))
        res[jsn['datatype']].append(jsn)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
            
def read_temptype(request):
    keyword = request.GET.get('keyword')
    res = []
    if keyword:
        dt = Template.objects.filter(temptype__icontains=keyword).values('temptype').distinct()
    else:
        dt = Template.objects.all().values('temptype').distinct()
    for t in dt:
        res.append(t['temptype'])
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
    
def savetemp(request):
    if request.method == 'POST':
        userid = request.COOKIES['id']
        ttype = request.POST.get('Modeltype','')
        if ttype.strip() <> '':
            temptype = ttype
        else:
            temptype = '未分类'
        status = request.POST.get('Mstatus')
        divdata = request.POST.get('Mhtml')
        tname = request.POST.get('tempname','')
        if tname.strip() <> '':
            tempname = tname
        else:
            tempname = '未命名'
        tmp = Template(userid = userid,tempid = uuid.uuid1(),status = status
                       ,divdata=divdata,temptype = temptype,tempname=tempname)
        tmp.save()
        divurl = 'http://' + request.META['HTTP_HOST'] + reverse('bi:body',args = (str(tmp.id),))
        tmp.divurl = divurl
        tmp.htmldata = tmp.htmldata.replace('<body >','<body id="i%s">' % str(tmp.id))
        tmp.save()
        return HttpResponse(divurl)
    else:
        return HttpResponse('is error') 

def getbody(request,htmlid):
    title = Template.objects.get(id=int(htmlid)).tempname
    title = 'Visio分析' if title == '' else title
    return render_to_response('bi/publish.html',{'id':htmlid,'title':title})

def getdiv(request):
    if request.method == 'GET':
        status = request.GET.get('Mstatus')
        temptype = request.GET.get('Modeltype')
        id = request.GET.get('id')
        res = []
        if status == '0':
            src = Template.objects.get(id = id)
            div = src.divdata.strip()
            response = HttpResponse(div)
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Headers"] = "*"
            return response
        elif temptype <> None:
            userid = request.COOKIES['id']
            src = Template.objects.filter(userid = userid,temptype = temptype,)
            for s in src:
                jsn = {}
                tempid = s.tempid
                status = s.status
                tempname = s.tempname
                temptype = s.temptype
                savetime = s.savetime.strftime("%Y%m%d%H%M%S")
                data = s.data
                jsn ['tempid'] = tempid
                jsn ['status'] = status
                jsn ['tempname'] = tempname
                jsn ['temptype'] = temptype
                jsn ['savetime'] = savetime
                jsn ['data'] = data
                res.append(jsn)
            response = HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Headers"] = "*"
            return response
    else:
        return HttpResponse('is error')

def get_json(request):
    chartid = request.POST.get('chartid')
    selpostdata = request.POST
    chart = User_data.objects.get(chartid=chartid)
    src = Source.objects.get(sourceid=chart.srcid)
    if chart.data <> '':
        jsn = chart.data.read()
        return HttpResponse(jsn)
    jsinfo = Echarts_Json_info.objects.get(chartid=chartid)
    sql = jsinfo.report_sql
    sql = sql.replace(' where 1=1 ',' where 1=1 ' + where_rule_info(selpostdata))
    data = []
    datalv = []
    series = []
    jsn = {}
    if jsinfo.flag == '11':
            for row in MySql.sel_table(sql,src.sourceip,src.sourceuser,src.sourcepasswd,src.sourceport):
                datalv.append(row)
            datalegend = {}
            xcols = []
            for row in datalv:
                if not datalegend.get(row[1]):
                    datalegend[row[1]] = []
                if row[0] not in xcols:
                    xcols.append(row[0])
            
            for d in datalegend:
                for i in range(len(xcols)):
                    datalegend[d].append('')
            
            for row in datalv:
                datalegend[row[1]][xcols.index(row[0])] = row[2]
                    
            for l in datalegend:
                srs={} 
                srs['data'] = datalegend[l]
                srs['name'] = l
                srs['type'] = ''
                srs['unit'] = jsinfo.lyunit
                srs['yAxisIndex'] = ''
                series.append(srs)
            jsn['yname'] = datalegend.keys()
            jsn['xAxis'] = xcols 
    elif jsinfo.flag == '1':
        y = Echarts_Json_columns.objects.filter(chartid=chartid,xAxis_or_yAxis='y').order_by('scaler')
        for l in range(len(y)+1):
            data.append([])

        for row in MySql.sel_table(sql,src.sourceip,src.sourceuser,src.sourcepasswd,src.sourceport):
            for r in range(len(row)):
                data[r].append(row[r])
        
        for i in range(len(data)-1):
            srs = {}
            numdata = []
            for n in data[i+1]:
                numdata.append(float(n))
            srs['data'] = numdata if chart.rttype == '' else []
            srs['name'] = y[i].echart_columns
            srs['type'] = y[i].chart_type
            srs['unit'] = jsinfo.lyunit if y[i].yAxisIndex == '0' else jsinfo.ryunit
            srs['yAxisIndex'] = y[i].yAxisIndex
            series.append(srs)    
        jsn['yname'] = [yname.echart_columns for yname in y]    
        jsn['xAxis'] =  data[0] if chart.rttype == '' else []
    elif jsinfo.flag == '2': 
        y = Echarts_Json_columns.objects.get(chartid=chartid,xAxis_or_yAxis='y')
        seriesname = y.echart_columns
        yname = []
        data = []
        for row in MySql.sel_table(sql,src.sourceip,src.sourceuser,src.sourcepasswd,src.sourceport):
            jsn2 = {}
            jsn2['name'] = row[0]
            jsn2['value'] = row[1]
            jsn2['seriesname'] =seriesname
            yname.append(row[0])
            data.append(jsn2)
        jsn['yname'] = yname
        jsn['data']=data
    elif jsinfo.flag == '3':
        y = Echarts_Json_columns.objects.get(chartid=chartid,xAxis_or_yAxis='y')
        where = y.where_rule +'  '+  where_rule_info(selpostdata)
        sql2 ='select distinct  %s from %s  %s order by %s' %(y.echart_columns,y.tablename,where,y.echart_columns)
        ys = [row[0] for row in MySql.sel_table(sql2)]
        xs = []
        alldata = {}
        for row in MySql.sel_table(sql,src.sourceip,src.sourceuser,src.sourcepasswd,src.sourceport):
            if not alldata.get(row[0]):
                alldata[row[0]] = {}
            alldata[row[0]][row[1]] = float(row[2])
            
            if row[0] not in xs:
                xs.append(row[0])
        for i in xs:
            for j in ys:
                tmp = []
                tmp.append(ys.index(j))
                tmp.append(xs.index(i))
                tmp.append(alldata.get(i).get(j,''))
                series.append(tmp)     
        jsn['yname'] = ys
        jsn['xAxis'] = xs    
    elif  jsinfo.flag =='21':
        y = Echarts_Json_columns.objects.filter(chartid=chartid,xAxis_or_yAxis='y').order_by('scaler') 
        seriesname ='总计'.encode('utf-8')
        yname = []
        data = []
        for  i  in y:
            yname.append(i.echart_columns)
        for row in MySql.sel_table(sql,src.sourceip,src.sourceuser,src.sourcepasswd,src.sourceport):
            for i in range(len(row)):
                jsn2 = {}
                jsn2['name'] = yname[i]
                jsn2['value'] = row[i]
                data.append(jsn2)
        jsn['seriesname'] =seriesname
        jsn['yname'] = yname 
        jsn['data']=data                                             
    print sql         
    jsn['title'] = jsinfo.title
    jsn['subtext'] = jsinfo.subtext
    jsn['xunit'] = jsinfo.xunit
    jsn['lyunit'] = jsinfo.lyunit
    jsn['ryunit'] = jsinfo.ryunit
    jsn['formatter'] = ''
    jsn['lyname'] = ''
    jsn['ryname'] = ''
    jsn['series'] = series
    return HttpResponse(json.dumps(jsn,indent = 2,ensure_ascii=False))
    
    
def del_chart(request):
    chartid = request.POST.get('chartid')
    ud = User_data.objects.get(chartid=chartid)
    ud.delete()
    return HttpResponse('ok')

def del_source(request):
    sourceid = request.POST.get('sourceid')
    us = Source.objects.get(sourceid=sourceid)
    us.delete()
    return HttpResponse('ok')

def get_urls(request):
    userid = request.GET.get('userid')
    temps = Template.objects.filter(userid=userid)
    res = {}
    for temp in temps:
        if not res.get(temp.temptype):
            res[temp.temptype] = []
        url = {}
        url['urlid'] = str(temp.id)
        url['urlname'] = temp.tempname
        url['url'] = temp.divurl
        url['urldate'] = temp.savetime.strftime('%Y-%m-%d %H:%M:%S')
        res[temp.temptype].append(url)
    return HttpResponse(json.dumps(res,indent = 2,ensure_ascii=False))

def update_url(request):
    urlid = request.POST.get('urlid')
    urlname = request.POST.get('urlname')
    urltype = request.POST.get('urltype')
    t = Template.objects.get(id=int(urlid))
    t.tempname = urlname
    t.temptype = urltype
    t.save()
    return HttpResponse('ok')

def del_url(request):
    urlid = request.POST.get('urlid')
    Template.objects.get(id=int(urlid)).delete()
    return HttpResponse('ok')

def gettest1(request):
    return render_to_response('bi/page1.html')

def gettest2(request):
    return render_to_response('bi/page2.html')

def gettest3(request):
    return render_to_response('bi/page3.html')






