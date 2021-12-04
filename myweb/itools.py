# -*- coding:utf-8 -*-
import MySQLdb
import time
import stripe
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import requests
import datetime
import json
import hashlib


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
    print params
    res = requests.get(url, params)

    print res.status_code, res.json()

class MySql(object):
    
    _ip = "127.0.0.1"
    _user = "root"
    _passwd = "gfpeitfklkimg@9527"
    _port = 3306
    _database = "app"
    
    @classmethod
    def mk_sql(cls,tab,inputdata):
        """输入表名、一条list记录，返会insert SQL"""
        sql = "insert into %s values(" % tab
        i = 1
        for data in inputdata:
            if data == None:
                col = 'null'
            else:
                col = '\'' + data + '\''
            sql = sql + col
            if i <> len(inputdata):
                sql = sql + ','
            i += 1
        sql = sql + ');'
        return sql
    
    @classmethod
    def conn_mysql(cls,ip = None, user = None, passwd = None,port = None):
        db = ''
        if ip == None and user == None and passwd == None and port == None:
            db = MySQLdb.connect(host = MySql._ip, user = MySql._user, passwd = MySql._passwd,port = MySql._port, db = MySql._database,charset='utf8')
        else:
            db = MySQLdb.connect(host = ip, user = user, passwd = passwd,port = int(port),charset='utf8')
        return db
    
    @classmethod
    def data_integrity(cls,userid):
        sql = """
        SELECT CONCAT(FORMAT((CASE WHEN LENGTH(a.username) > 0 THEN 1 ELSE 0 END+
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
        CASE WHEN LENGTH(a.corp) > 0 THEN 1 ELSE 0 END)/17,2)*100,'%%')
        FROM app.app_userinfo a
        WHERE a.userid = '%s'
        """ % userid
        return MySql.sel_table(sql).next()[0]
    
    @classmethod
    def has_result(cls,sql):
        re = False
        db = MySql.conn_mysql()
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) > 0:
            re = True
        db.close()
        return re
    
    @classmethod
    def sel_table(cls,sql):
        db = MySql.conn_mysql()
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            row8 = []
            for r in row:
                if r == None:
                    row8.append(r)
                else:
                    row8.append(unicode(r)) #.encode('utf8')
            yield row8
        db.close()
        
    @classmethod
    def run_sql(cls,sqls):
        db = MySql.conn_mysql()
        cursor = db.cursor()
        try:
            cursor.execute(sqls)
            db.commit()
        except:
            db.rollback()
            print sqls
            print "run sql failed!\n"
        
        db.close()

    @classmethod
    def exec_sql(cls,db,sqls):
        cursor = db.cursor()
        try:
            cursor.execute(sqls)
            db.commit()
            print "run sql done!\n"
        except MySQLdb.Error,e:
            db.rollback()
            print sqls
            print "run sql failed!\n",e[0],e[1]
    
    @classmethod
    def close_db(cls,db):
        db.close()

    @classmethod
    def read_tab_ofdb(cls,db):
        db = MySql.conn_mysql()
        db.select_db('information_schema')
        cursor = db.cursor()
        cursor.execute('''SELECT TABLE_NAME FROM TABLES WHERE table_schema = '%s' AND table_type = 'BASE TABLE';''' % db)
        tabs = []
        for tab in cursor.fetchall():
            tabs.append(tab[0])
        return tabs
    
    @classmethod
    def read_dbtree(cls,ip,user,passwd,port):
        db = MySql.conn_mysql(ip=ip,user=user,passwd=passwd,port=port)
        cursor = db.cursor()
        dbtree = {}
        try:
            cursor.execute('show databases;')
            dbnames = cursor.fetchall()
            for d in dbnames:
                tabs = []
                dbname = d[0]
                cursor.execute('use information_schema;')
                cursor.execute('''SELECT TABLE_NAME FROM TABLES WHERE table_schema = '%s' AND table_type = 'BASE TABLE';''' % dbname)
                for tab in cursor.fetchall():
                    tabs.append(tab[0])
                dbtree[dbname] = tabs
            return dbtree
        except MySQLdb.Error,e:
            db.rollback()
            print "MySQL Error %d: %s" % (e.args[0], e.args[1])
        cursor.close()
        db.close()
        
    @classmethod   
    def creata_tab(cls,host,user,passwd,port, dbname, tabname,own_tab):
        db = MySql.conn_mysql(host, user, passwd, port)
        cursor = db.cursor()
        try:
            cursor.execute('use %s;' % dbname)
            cursor.execute('SHOW CREATE TABLE  %s.%s;' % (dbname,tabname))
            ddl = cursor.fetchall()[0][1]
            ddl = ddl.split('\n',1)
            a = ddl[0].replace('TEMPORARY ','').replace(tabname,own_tab)
            myddl = a+'\n'+ddl[1]
            mydb = MySql.conn_mysql()
            mydb.select_db(MySql._database)
            cur = mydb.cursor()
#             cur.execute('drop table if exists %s' % own_tab)
            cur.execute(myddl)
            
            def sel_tab():
                cursor.execute('select * from %s' % tabname)
                for row in cursor.fetchall():
                    row8 = []
                    for r in row:
                        if r == None:
                            row8.append(r)
                        else:
                            row8.append(unicode(r).encode('utf8'))
                    yield row8
                    
            for row in sel_tab():
                sql = MySql.mk_sql(own_tab, row)
                cur.execute(sql)
                mydb.commit()
            db.close()
            mydb.close()
        except MySQLdb.Error, e:
            print "MySQL Error %d: %s" % (e.args[0], e.args[1])
            
    @classmethod
    def read_tab(cls, tabname):
        db = MySql.conn_mysql()
        cursor = db.cursor()
        table_inf = {}
        table_inf['tabname'] = tabname
        try:
            cursor.execute('use information_schema;')
            cursor.execute("SELECT TABLE_NAME,DATA_LENGTH,TABLE_ROWS FROM TABLES WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (MySql._database, tabname))
            table_size_num = cursor.fetchall()
            table_inf['size'] = table_size_num[0][1]
            table_inf['count'] = table_size_num[0][2]
            cursor.execute("SELECT TABLE_NAME,UPDATE_TIME FROM information_schema.tables where TABLE_SCHEMA='%s' and TABLE_NAME='%s';" % (MySql._database, tabname))
            table_update = str(cursor.fetchall()[0][1])
            table_inf['update'] = table_update
            cursor.execute('use information_schema;')
            cursor.execute('''select column_name,data_type from columns where table_name = '%s';''' % tabname)
            table_data_type = [(res[0], res[1]) for res in cursor.fetchall()]
            list_num_type = ['tinyint', 'smallint', 'mediumint', 'int', 'bigint', 'float', 'double', 'decimal']
            list_date_type = ['date', 'datetime', 'timestamp', 'time', 'year']
            table_inf['num'] = []
            table_inf['date'] = []
            table_inf['text'] = []
            
            for t in table_data_type:
                if t[1] in list_num_type:
                    table_inf['num'].append(t[0])
                elif t[1] in list_date_type:
                    table_inf['date'].append(t[0])
                else:
                    table_inf['text'].append(t[0])
            return table_inf
        except MySQLdb.Error, e:
            print "MySQL Error %d: %s" % (e.args[0], e.args[1])
    
def get_now(times=None,addday=None,addtype=None):
    if times ==None and addday == None:
        return  time.strftime("%Y%m%d%H%M%S", time.localtime(int(time.time())))
    times = times if len(times) == 14 else times + '000000'
    tar = ''
    now = datetime.datetime.strptime(times,"%Y%m%d%H%M%S")
    if addtype == 'd' or addtype == None:
        tar = now + datetime.timedelta(days = int(addday) if addday else 0)
    elif addtype == 'h':
        tar = now + datetime.timedelta(hours = int(addday) if addday else 0)
    elif addtype == 'm':
        tar = now + datetime.timedelta(minutes = int(addday) if addday else 0)
    elif addtype == 'w':
        tar = now + datetime.timedelta(weeks = int(addday) if addday else 0)
    else:
        return '-1'
    return datetime.datetime.strftime(tar,"%Y%m%d%H%M%S")

def get_date():
    d = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(int(time.time()))).split('-')
    res = {}
    res['y'] = d[0]
    res['m'] = d[1]
    res['d'] = d[2]
    res['H'] = d[3]
    res['M'] = d[4]
    res['S'] = d[5]
    return res

def get_title(listingid):
    sql = """
            SELECT listingid,descrition,price,CAST(bedroom AS SIGNED),CAST(toilet AS SIGNED)
            FROM app.app_listing
            LEFT JOIN app.t99_cityname
            ON cityname = codename
            WHERE listingid = '%s'
          """ % listingid
    title = ''
    for row in MySql.sel_table(sql):
        title = "[%s新盘]%s|%s房%s卫|MLS#:%s" % (row[1],row[2],row[3],row[4],row[0].upper())
    return title

def get_code(codetab,codename):
    row = MySql.sel_table("select cityname from %s where srcdata='%s'" % (codetab,codename))
    cn = codename
    for r in row:
        cn = r[0]
    return cn

def get_housetype_name(housetype):
    row = MySql.sel_table("select typename from app.t99_housetype where srcdata='%s'" % housetype)
    cn = housetype
    for r in row:
        cn = r[0]
    return cn
    
def get_cityname(cityid):
    row = MySql.sel_table("select cityname from app.t99_cityname where cityid='%s'" % cityid)
    cn = '温哥华'
    for r in row:
        cn = r[0]
    return cn

def get_countyname(countyid):
    row = MySql.sel_table("select countyname from app.t99_cityname where countyid='%s'" % countyid)
    cn = '加拿大'
    for r in row:
        cn = r[0]
    return cn

def get_counties(cityid):
    row = MySql.sel_table("select distinct countyid,countyname from app.t99_cityname where cityid='%s' and countyid is not null" % cityid)
    cities = []
    for r in row:
        cities.append({'countyid':r[0],'countyname':r[1]})
    return cities
def get_cities(group):
    row = MySql.sel_table("select distinct cityid,cityname from app.t99_cityname where groupid='%s' and countyid is not null" % group)
    cities = []
    for r in row:
        cities.append({'cityid':r[0],'cityname':r[1]})
    return cities
def get_groups(prov):
    row = MySql.sel_table("select distinct groupid,groupname from app.t99_cityname where provid='%s' and countyid is not null" % prov)
    cities = []
    for r in row:
        cities.append({'groupid':r[0],'groupname':r[1]})
    return cities
def get_provs(country):
    row = MySql.sel_table("select distinct provid,provname from app.t99_cityname where countryid='%s' and countyid is not null" % country)
    cities = []
    for r in row:
        cities.append({'provid':r[0],'provname':r[1]})
    return cities
def get_countries():
    row = MySql.sel_table("select distinct countryid,countryname from app.t99_cityname")
    cities = []
    for r in row:
        cities.append({'countryid':r[0],'countryname':r[1]})
    return cities

def get_des(codetab,codename):
    row = MySql.sel_table("select descrition from %s where codename='%s'" % (codetab,codename))
    cn = codename
    for r in row:
        cn = r[0]
    return cn

def get_code2(codetab,codename):
    row = MySql.sel_table("select descrition2 from %s where codename='%s'" % (codetab,codename))
    cn = codename
    for r in row:
        cn = r[0]
    return cn

def get_code3(codetab,codename):
    row = MySql.sel_table("select codename from %s where descrition2='%s'" % (codetab,codename))
    cn = codename
    for r in row:
        cn = r[0]
    return cn

def charge_by_stripe(token,amt,curr):
    stripe.api_key = 'sk_live_qU4vWKnLESpNk1CBMYZXY2Vp'
    try:
        stripe.Charge.create(
                amount = int(int(amt)*1.05),
                currency = curr,
                source = token,
                description = 'charge rainzure')
        return 'ok'
    except stripe.error.CardError as e:
        print e.code
        return e.code

def filter_listing(price1,price2,ltype,bedroom,toilet,lstyle):
    def get_type(sty):
        if len(sty) == 0:
            return ''
        elif len(sty) == 1:
            return "AND descrition in ('%s')" % sty[0]
        else:
            andsql = "AND descrition in ('%s'" % sty[0]
            for t in sty[1:]:
                andsql = andsql + ",'%s'" % t
        andsql = andsql + ')'
        return andsql
    if price1 == None:
        price1 = 0
    if price2 == None:
        price2 = 99999999999
    if bedroom == None:
        bedroom = 0
    if toilet == None:
        toilet =0
    lstyle ='listing1'
        
    sty = lstyle.split('or')
    sql = ''
    if ltype == 'listing1':
        sql = """
            SELECT listingid
            FROM app.app_listing
            INNER JOIN app.t99_housetype
            ON housetype = codename
            WHERE CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) BETWEEN %s AND %s
            AND CAST(bedroom AS SIGNED) >= %s
            AND CAST(toilet AS SIGNED) >= %s
            %s
            limit 100
        """ % (price1,price2,bedroom,toilet,get_type(sty))
    elif ltype == 'listing2':
        sql = """
            SELECT listingid
            FROM app.app_listing2
            INNER JOIN app.t99_housetype
            ON housetype = codename
            WHERE CAST(REPLACE(REPLACE(price1,'$',''),',','') AS SIGNED) >=%s
            AND CAST(REPLACE(REPLACE(price1,'$',''),',','') AS SIGNED) <=%s
            %s
            limit 100
        """ % (price1,price2,get_type(sty))
    listings = []
    print sql
    for row in MySql.sel_table(sql):
        listings.append(row[0])

    return listings
            
def authed_user():
    sql = "SELECT userid FROM app.app_userinfo WHERE LENGTH(creditcard) = 16"       
    userids = []
    for row in MySql.sel_table(sql):
        userids.append(row[0])
    return userids

def pay(userid,srtype,tr,paynow):
    if srtype == 'article':
        sql = """
                SELECT couponid,amt FROM app.app_coupon
                WHERE userid = '%s'
                AND usable = '1'
                AND coupontype = 'b'
                AND enddt >= NOW()
              """ % userid
        for row in MySql.sel_table(sql):
            if int(row[1]) >= 1:
                if paynow or tr == '1':
                    sql2 = """
                            update app.app_coupon set amt=amt-1
                            where couponid=%s
                           """ % row[0]
                    MySql.run_sql(sql2)
                return True
            
    fee = 0
    if tr == '0' and srtype in ('listing1'):
        fee = 2.99
    elif tr == '0' and srtype in ('article'):
        fee = 0.99
    elif tr == '1' and srtype in ('listing1','listing2','mysite'):
        fee = 29.99
    else:
        return True
    
    sql = """
            SELECT sum(amt) FROM app.app_coupon
            WHERE userid = '%s'
            AND usable = '1'
            AND coupontype in ('a','c','d')
            AND enddt >= NOW()
          """ % userid
    sums = MySql.sel_table(sql).next()[0]
    allcp = 0 if sums == None else sums
    
    sql = """
            select bal from app.app_userinfo where userid='%s'
          """ % userid
    bal = float(MySql.sel_table(sql).next()[0])
    if (bal+float(allcp)) > fee:
        sqlcp = """
                SELECT couponid,amt FROM app.app_coupon
                WHERE userid = '%s'
                AND usable = '1'
                AND coupontype in ('a','c','d')
                AND enddt >= NOW()
              """ % userid
        for row in MySql.sel_table(sqlcp):
            amt = float(row[1])
            if amt-fee >= 0:
                if paynow or tr == '1':
                    sql2 = """
                            update app.app_coupon set amt=%s
                            where couponid=%s
                           """ % (amt-fee,row[0])
                    MySql.run_sql(sql2)
                return True
            else:
                sql2 = """
                        update app.app_coupon set amt=0
                        where couponid=%s
                       """ % row[0]
                MySql.run_sql(sql2)
                fee = fee - amt
        if bal >= float(fee):
            if paynow or tr == '1':
                sql3 = """
                         update app.app_userinfo set bal=%s
                         where userid='%s'
                       """ % (str(bal-float(fee)),userid)
                MySql.run_sql(sql3)
            return True
        else:
            return False
    else:
        return False

def send_mail_vcode(userid,keynum):
    # 第三方 SMTP 服务
    mail_host="smtp.realtoraccess.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Yjh932320908"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = [userid]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("瑞安居", 'utf-8')
    message['To'] =  Header(userid, 'utf-8')
    #标题
    subject = '瑞安居-密码修改'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''<p>尊敬的用户<b> %s</b>，您好！</p>
<p>感谢您选择瑞安居，我们致力于为海外房产经纪人提供便利的房源分享服务！</p>
<p>您的临时新密码为：<b>%s</b></p>
<br>
<p>瑞安居友情提示您请立即登陆瑞安居，进入我的-设置 页面完成密码修改，并妥善保管您的新密码。</p>
<p>瑞安居</p>
<p>海外买家一触即发！</p>
<br>
<br>
<img src="cid:image1">
    ''' % (userid,keynum)
    msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))
    fp = open(r'/root/myweb/static/img/mail.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)
    try:
        smtpObj = smtplib.SMTP() 
    #     smtpObj = SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print e,"Error: 无法发送邮件"

def send_invoice(userid):
    # 第三方 SMTP 服务
    mail_host="smtp.realtoraccess.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Yjh932320908"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = [userid]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("瑞安居", 'utf-8')
    message['To'] =  Header(userid, 'utf-8')
    #标题
    subject = '您的发票将为您尽快开出！'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''<p>尊敬的用户<b> %s</b>，您好！</p>
<p>感谢您选择瑞安居，我们致力于为海外房产经纪人提供便利的房源分享服务！</p>
<p>我们已经收到您要求寄送发票的需求，会以电子邮件方式尽快为您发送至您的邮箱：%s，请您耐心等待。欢迎您随时联络我们，电子邮件：clientservice@realtoraccess.com，我们将竭诚为您服务。</p>
<br>
<p>瑞安居</p>
<p>海外买家一触即发！</p>
<br>
<br>
<img src="cid:image1">
    ''' % (userid,userid)
    msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))
    fp = open(r'/root/myweb/static/img/mail.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)
    try:
        smtpObj = smtplib.SMTP() 
    #     smtpObj = SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print e,"Error: 无法发送邮件"

def send_spread(userid,orderid):
    # 第三方 SMTP 服务
    mail_host="smtp.realtoraccess.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Yjh932320908"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = [userid]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("瑞安居", 'utf-8')
    message['To'] =  Header(userid, 'utf-8')
    #标题
    subject = '即将为您翻译房源，进行房源推广！'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''<p>尊敬的用户<b> %s</b>，您好！</p>
<p>我们已经收到您的中文推广要求，您的订单号是:%s，您可以在海外房源推广目录下查看订单状态，评价我们的服务。</p>
<p>接下来，我们将首先为您进行房源翻译，翻译后的房源可以在目录【推广中】查看并供您自由分享。同时我们还将为您嫁接瑞安居自有推广团队，帮您实现最大限度的房源曝光。</p>
<br>
<p>瑞安居</p>
<p>海外买家一触即发！</p>
<br>
<br>
<img src="cid:image1">
    ''' % (userid,orderid)
    msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))
    fp = open(r'/root/myweb/static/img/mail.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)
    try:
        smtpObj = smtplib.SMTP() 
    #     smtpObj = SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print e,"Error: 无法发送邮件"

def send_private_custom(userid):
    # 第三方 SMTP 服务
    mail_host="smtp.realtoraccess.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Yjh932320908"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = [userid]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("瑞安居", 'utf-8')
    message['To'] =  Header(userid, 'utf-8')
    message['Bcc'] =  Header('yujh@realtoraccess.com,jhyu@ikingcity.cn', 'utf-8')
    #标题
    subject = '免费-私享-无忧，即将为您开启海外房源订制之旅！'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''<p>尊敬的用户<b> %s</b>，您好！</p>
<p>感谢您选择瑞安居，我们已经收到您的私人订制要求，瑞安居是海外房产经纪对接全球华人买家的房源分享平台。平台提供最及时的海外房源发布功能，通过大数据技术，将您的房源订制要求与海外经纪人信用以及适合房源相匹配，帮您找到最靠谱的经纪和最适合的房源。</p>
<p>您可以在我的-订制房源中查看推荐房源，您也可以通过在线沟通功能与房源经纪人进行联系，整个过程完全免费，让您私享最及时、优质、可靠的海外置业信息服务。</p>
<br>
<p>瑞安居</p>
<p>私享、免费、无忧</p>
<br>
<br>
<img src="cid:image1">
    ''' % userid
    msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))
    fp = open(r'C:\Users\Administrator\Pictures\mail.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)
    try:
        smtpObj = smtplib.SMTP() 
    #     smtpObj = SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print e,"Error: 无法发送邮件"

def send_auth(userid):
    # 第三方 SMTP 服务
    mail_host="smtp.realtoraccess.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Yjh932320908"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = [userid]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("瑞安居", 'utf-8')
    message['To'] =  Header(userid, 'utf-8')
    #标题
    subject = '恭喜您通过海外经纪人身份验证！'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''<p>尊敬的用户<b> %s</b>，您好！</p>
<p>  恭喜您通过海外经纪人身份验证，已为您充值16.95元礼券，您可以点击我的钱包-优惠券进行查看，体验我们的服务时，16.95元礼券将被首先扣除，您可以免费分享5个房源，或者免费分享17个热点文章。</p>
<p>  我们为经过身份验证的海外经纪人提供房源推广服务，依托瑞安居自有华人推广团队，帮您转发房源，推荐适合的房地产潜在买家。</p>
<p>  针对您要推广的房源，您可以在房源分享下点击【我要推广】控件，体验我们的服务，提升海外房源曝光度。</p>
<br>
<p>瑞安居</p>
<p>海外买家一触即发！</p>
<br>
<br>
<img src="cid:image1">
    ''' % (userid)
    msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))
    fp = open(r'/root/myweb/static/img/mail.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)
    try:
        smtpObj = smtplib.SMTP() 
    #     smtpObj = SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print e,"Error: 无法发送邮件"

def send_welcome(userid):
    # 第三方 SMTP 服务
    mail_host="smtp.realtoraccess.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Yjh932320908"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = [userid,'zhc@realtoraccess.com','yujh@realtoraccess.com','dxc@realtoraccess.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("瑞安居", 'utf-8')
    message['To'] =  Header(userid, 'utf-8')
    message['Bcc'] = 'zhc@realtoraccess.com,yujh@realtoraccess.com,dxc@realtoraccess.com'
    #标题
    subject = '欢迎您成为瑞安居注册用户'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''<p>尊敬的用户<b> %s</b>，您好！</p>
<br>
<p>感谢您选择瑞安居，我们致力于为海外房产经纪人提供便利的房源分享服务！</p>
<p>瑞安居是海外房产经纪推广个人品牌，对接全球华人买家的房源分享平台。平台提供最及时的海外房源发布功能，实现海外房源无忧分享，通过大数据技术，将海外经纪人个人品牌与海量热门文章嫁接，实现最大限度的经纪人品牌曝光。</p>
<p>您分享的内容除了可以方便的发布在自己的朋友圈和微信好友，我们还将帮助您进行海外房源推广，将您发布的房源转发给瑞安居自有华人推广团队，华人买家可以通过我们的在线沟通功能与您取得联系，进行咨询。</p>
<p>海外经纪人注册并验证，可获取16.95元礼券，免费分享经纪人主页，您只需用您的邮箱账户登陆APP，设置个人信息和模板，即可开启您的房源分享之旅，找到海外买家一触即发！</p>
<br>
<p>瑞安居</p>
<br>
<br>
<img src="cid:image1">
    ''' % (userid)
    msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))
    fp = open(r'/root/myweb/static/img/mail.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)
    try:
        smtpObj = smtplib.SMTP() 
    #     smtpObj = SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print e,"Error: 无法发送邮件"

def send_code(userid,token):
    # 第三方 SMTP 服务
    mail_host="smtp.mxhichina.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Ra123456"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = [userid]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("瑞安居", 'utf-8')
    message['To'] =  Header(userid, 'utf-8')
    #标题
    subject = '您正在修改密码-瑞安居'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''<p>尊敬的用户<b> %s</b>，您好！</p>
<br>
<p>您的验证码是：</p>
<h1>%s</h1>
<br>
<p>瑞安居</p>
<br>
<br>
<img src="cid:image1">
    ''' % (userid,token)
    msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))
    fp = open(r'/root/myweb/static/img/mail.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)
    try:
        smtpObj = smtplib.SMTP() 
    #     smtpObj = SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print e,"Error: 无法发送邮件"


def send_usermsg(info):
    # 第三方 SMTP 服务
    mail_host="smtp.realtoraccess.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Yjh932320908"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = [info.userid,'zhc@realtoraccess.com','yujh@realtoraccess.com','dxc@realtoraccess.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("瑞安居", 'utf-8')
    message['To'] =  Header(info.userid, 'utf-8')
    message['Bcc'] = 'zhc@realtoraccess.com,yujh@realtoraccess.com,dxc@realtoraccess.com'
    #标题
    subject = '有人需要看房，请安排经纪'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''<p>您好！</p>
<br>
<p>用户(%s)提交了看房申请，房源号为：%s，他的联系方式如下：</p>
<p>电话：%s</p>
<p>留言：%s</p>
<br>
<p>瑞安居</p>
<br>
<br>
<img src="cid:image1">
    ''' % (info['name'],info['mls'],info['tel'],info['msg'])
    msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))
    fp = open(r'/root/myweb/static/img/mail.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)
    try:
        smtpObj = smtplib.SMTP() 
    #     smtpObj = SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print e,"Error: 无法发送邮件"

def send_custom(receivers,mailbody):
    # 第三方 SMTP 服务
    mail_host="smtp.realtoraccess.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Yjh932320908"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = receivers  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEText(mailbody, 'plain', 'utf-8')
    message['From'] = Header("瑞安居", 'utf-8')
#     message['To'] =  Header("测试", 'utf-8')
    #标题
    subject = '瑞安居-收到了新的私人定制订单'
    message['Subject'] = Header(subject, 'utf-8')
      
      
    try:
        smtpObj = smtplib.SMTP() 
    #     smtpObj = SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print e,"Error: 无法发送邮件"

def send_sp_getstart(info):
    # 第三方 SMTP 服务
    mail_host="smtp.realtoraccess.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Yjh932320908"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = ['service@webmainland.com','yjh@webmainland.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("webmainland", 'utf-8')
    message['To'] =  Header('service@webmainland.com', 'utf-8')
    message['Bcc'] = 'yjh@webmainland.com'
    #标题
    subject = '一个新的SinglePage订单（来自门户网站）'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''<p>您好！订单信息如下(Free Trial)：</p>
<br>
<p>First Name：%s</p>
<p>Last Name：%s</p>
<p>Email：%s</p>
<p>MLS：%s</p>
<p>Phone：%s</p>
<p>Company Name：%s</p>
<p>Address：%s</p>
<p>Post Code：%s</p>
<br>
<p>Webmainland</p>
<br>
<br>
    ''' % (info['fname'],info['lname'],info['email'],info['mls'],info['tel'],info['corp'],info['address'],info['postid'])
    msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))

    try:
        smtpObj = smtplib.SMTP() 
    #     smtpObj = SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print e,"Error: 无法发送邮件"

def send_sp_signup(info):
    # 第三方 SMTP 服务
    mail_host="smtp.realtoraccess.com"  #设置服务器
    mail_user="clientservice@realtoraccess.com"    #用户名
    mail_pass="Yjh932320908"   #口令 
    sender = 'clientservice@realtoraccess.com'
    receivers = ['service@webmainland.com','yjh@webmainland.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #正文
    message = MIMEMultipart('related')
    message['From'] = Header("webmainland", 'utf-8')
    message['To'] =  Header('service@webmainland.com', 'utf-8')
    message['Bcc'] = 'yjh@webmainland.com'
    #标题
    subject = '一个新的用户注册了！（来自门户网站）'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    body = '''<p>您好！用户信息如下(Buyer Report)：</p>
<br>
<p>Name：%s</p>
<p>Email：%s</p>
<br>
<br>
    ''' % (info['name'],info['email'])
    msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))

    try:
        smtpObj = smtplib.SMTP() 
    #     smtpObj = SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print e,"Error: 无法发送邮件"

def send_mobile_vcode(tel,vcode):
    url = 'http://121.199.50.122:8888/sms.aspx'
    params = {}
    params['userid'] = '1670'
    params['account'] = 'HWRAJ'
    params['password'] = 'Hw123654'
    params['mobile'] = tel
    params['content'] = '您的手机正在注册瑞安居，验证码为:%s，5分钟内有效。【瑞安居】' % vcode
    params['sendTime'] = ''
    params['action'] = 'send'
    params['extno'] = ''
    res = requests.post(url,params=params)
    return res.content

def someone_subscribe():
    url = 'http://47.98.235.166:9918/sms.aspx'
    params = {}
    params['userid'] = '371'
    params['account'] = 'HWRAJ'
    params['password'] = 'Hw123654'
    params['mobile'] = '18210067493,18601356796'
    params['content'] = '【瑞安居】有人关注了大温的房价走势,请知悉。'
    params['sendTime'] = ''
    params['action'] = 'send'
    params['extno'] = ''
    res = requests.post(url,params=params)
    return res.content

def someone_leave_msg(userid):
    url = 'http://47.98.235.166:9918/sms.aspx'
    params = {}
    params['userid'] = '371'
    params['account'] = 'HWRAJ'
    params['password'] = 'Hw123654'
    params['mobile'] = '18210067493,18601356796'
    params['content'] = '【瑞安居】经纪人%s,有一条新的留言信息,请知悉。' % userid
    params['sendTime'] = ''
    params['action'] = 'send'
    params['extno'] = ''
    res = requests.post(url,params=params)
    return res.content

def third_party_signup(userid):
    url = 'http://47.98.235.166:9918/sms.aspx'
    params = {}
    params['userid'] = '371'
    params['account'] = 'HWRAJ'
    params['password'] = 'Hw123654'
    params['mobile'] = '18210067493,18601356796'
    params['content'] = '【瑞安居】经纪人%s,通过第三方渠道注册成功,请知悉。' % userid
    params['sendTime'] = ''
    params['action'] = 'send'
    params['extno'] = ''
    res = requests.post(url,params=params)
    return res.content

def get_token_hx():
    data = {}
    data['grant_type'] = 'client_credentials'
    data['client_id'] = 'YXA6xMmL8F3cEeahMGVBJEq9ww'
    data['client_secret'] = 'YXA6kBN90S-1otXhnZRtD8VHwgPmQAs'
    headers = {'Content-Type':'application/json'}
    jsn = json.dumps(data,indent = 2,ensure_ascii=False)
    res = requests.post('https://a1.easemob.com/ruianju/ruianju/token',data=jsn,headers=headers)
    return res.json()['access_token']

def signup_hx(hxid):
    data = {}
    data['username'] = str(hxid)
    data['password'] = 'raj123456'
    jsn = json.dumps(data,indent = 2,ensure_ascii=False)
    headers = {'Content-Type':'application/json','Authorization':'Bearer %s' % get_token_hx()}
    res = requests.post('https://a1.easemob.com/ruianju/ruianju/users',data=jsn,headers=headers)
    headers2 = {'Authorization':'Bearer %s' % get_token_hx()}
    res2 = requests.post('https://a1.easemob.com/ruianju/ruianju/chatgroups/258424278263792048/users/%s' % str(hxid),headers=headers2)
    if res.status_code == 200 and res2.status_code == 200:
        return 'ok'
    else:
        return 'err'

def send_msg_hx(target_type,target,msg,froms = None):
    #all 258424278263792048
    #send_msg_hx('chatgroups','258424278263792048','asd,http://www.realtoraccess.com/app/get/free/699,sddasd')
    #target_type: users chatgroups chatrooms
    data = {}
    data['target_type'] = target_type
    data['target'] = target
    data['msg'] = {}
    data['msg']['type'] = 'txt'
    data['msg']['msg'] = msg
    data['from'] = froms if froms <> None else '142'
    jsn = json.dumps(data,indent = 2,ensure_ascii=False)
    headers = {'Content-Type':'application/json','Authorization':'Bearer %s' % get_token_hx()}
    res = requests.post('https://a1.easemob.com/ruianju/ruianju/messages',data=jsn,headers=headers)
    if res.status_code == 200:
        return 'ok'
    else:
        return res.content

def translate_en2zh(q):
    para = {}
    para['q'] = q.replace('&','-').replace('+','﹢')
    para['from'] = 'en'
    para['to'] = 'zh'
    para['appid'] = '20180418000147575'
    para['salt'] = '8'
    
    m2 = hashlib.md5()
    m2.update(para['appid']+para['q']+para['salt']+'7pEluNjFFXFvPziakhSd')
    para['sign'] = m2.hexdigest()
    res = requests.get('http://api.fanyi.baidu.com/api/trans/vip/translate',params=para).json()
    if res.get('trans_result'):
        return res.get('trans_result')[0].get('dst')
    else:
        return ''
