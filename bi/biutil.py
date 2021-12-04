# -*- coding:utf-8 -*-
import json
import MySQLdb
import time
import xlrd
from pyhdfs import HdfsClient

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
    def conn_mysql(cls,ip = None, user = None, passwd = None,port = None,db=None):
        db = ''
        if (ip == None and user == None and passwd == None and port == None)\
            or (ip == '' and user == '' and passwd == '' and port == ''):
            db = MySQLdb.connect(host = MySql._ip, user = MySql._user, passwd = MySql._passwd,port = MySql._port, db = MySql._database,charset='utf8')
        else:
            db = MySQLdb.connect(host = ip, user = user, passwd = passwd,port = int(port), db = db,charset='utf8')
        return db
    
    @classmethod
    def sel_table(cls,sql,host=None,user=None,passwd=None,port=None):
        print sql
        db = MySql.conn_mysql(host,user,passwd,port)
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            row8 = []
            for r in row:
                if r == None:
                    row8.append(r)
                else:
                    row8.append(unicode(r))
            yield row8
        db.close()
        
    @classmethod
    def run_sql(cls,sqls):
        db = MySql.conn_mysql()
        cursor = db.cursor()
        try:
            cursor.execute(sqls)
            db.commit()
            print "run sql done!\n"
        except:
            db.rollback()
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
            print "run sql failed!\n",e[0],e[1]
    
    @classmethod
    def close_db(cls,db):
        db.close()

    @classmethod
    def read_tab_ofdb(cls,dbname):
        db = MySql.conn_mysql()
        db.select_db('information_schema')
        cursor = db.cursor()
        cursor.execute('''SELECT TABLE_NAME FROM TABLES WHERE table_schema = '%s' AND table_type = 'BASE TABLE';''' % dbname)
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
    def read_tab(cls,tabname,ip=None,user=None,passwd=None,port=None,dbname=None):
        db = MySql.conn_mysql(ip,user,passwd,port,dbname)
        cursor = db.cursor()
        dbname = dbname if dbname <> None and dbname <> '' else MySql._database
        table_inf = {}
        table_inf['tabname'] = tabname
        try:
            cursor.execute('use information_schema;')
            cursor.execute("SELECT TABLE_NAME,DATA_LENGTH,TABLE_ROWS FROM TABLES WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (dbname, tabname))
            table_size_num = cursor.fetchall()
            table_inf['size'] = table_size_num[0][1]
            table_inf['count'] = table_size_num[0][2]
            cursor.execute("SELECT TABLE_NAME,UPDATE_TIME FROM information_schema.tables where TABLE_SCHEMA='%s' and TABLE_NAME='%s';" % (dbname, tabname))
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
    
    @classmethod
    def create_excel_tab(cls,xlsfile,tabname):
        
        def isType(t):
            if t == 2:
                ctype = 'numeric(50,6)'
            elif t == 3 :
                ctype = 'datetime'          
            else :
                ctype = 'varchar(300)'
            return ctype
        
        xls = xlrd.open_workbook(xlsfile)
        sheet = xls.sheets()[0]
        nrows = sheet.nrows
        ncols = sheet.ncols
        cell_value = []
        cell_type = []
    
        for c in range(ncols):
            cell_value.append(sheet.cell_value(0,c))
            cell_type.append(sheet.cell_type(1,c))
    
            
        sql = 'create table %s(' % tabname
        for i in range(len(cell_type)):
            sql += ('`'+cell_value[i]+ '`' + ' ' + isType(cell_type[i]))
            if i < len(cell_type)-1:
                sql = sql + ','
        sql += ')ENGINE=InnoDB DEFAULT CHARSET=utf8;'
        print sql   
        
        db = MySql.conn_mysql()
        cursor = db.cursor()
        
        try:
#             cursor.execute('use mytest;')
#             cursor.execute('drop table if exists tabname;')
            cursor.execute(sql)
            
            insert_sql = 'insert into `%s` (' % tabname
            for j in range(0,ncols-1):
                insert_sql = insert_sql + '`%s`' % cell_value[j] + ','
            insert_sql = insert_sql + '`%s`' % cell_value[ncols - 1]
            insert_sql += ') values (' 
            for i in range(1,nrows):
                k = 0
                sql = insert_sql
                for j in range(ncols):
                    if k == 0:
                        if sheet.cell_type(i,j) == 3:
                            sql += "'%s'" % (xlrd.xldate.xldate_as_datetime(sheet.cell_value(i,j),0))
                        else:
                            sql += "'%s'" % (sheet.cell_value(i,j))
                    else:
                        if sheet.cell_type(i,j) == 3:
                            sql += ','+ "'%s'" % (xlrd.xldate.xldate_as_datetime(sheet.cell_value(i,j),0))
                        else:
                            sql += ','+ "'%s'" % (sheet.cell_value(i,j))
                    k +=1
                sql += ');'
                cursor.execute(sql)
                db.commit()
            
        except MySQLdb.Error,e:
                db.rollback()
                print "MySQL Error %d: %s" % (e.args[0], e.args[1])
        db.close()

class HDFS(object):
    
    _host = '123.57.184.16:50070'
    
    def __init__(self,host=None):
        if host:
            self.ip = host
        else:
            self.ip = HDFS._host
    
    def read_file(self,path,limit=None):
        c = HdfsClient(self.ip)
        content = ''
        i = 1
        for line in c.open(path):
            content += line
            if i == limit:
                return content
            i += 1
        return content

    
def mk_json(tabname,sql = None,colname = None):
    tab = []
    k = []
    v = []
    if sql == None:
        for row in MySql.sel_table('select * from %s' % tabname):
            v.append(row)
    else:
        for row in MySql.sel_table(sql):
            v.append(row)
        
    for row in MySql.sel_table("""SELECT * FROM information_schema.columns
    WHERE table_name = '%s'""" % tabname):
        k.append(row[3])  #,row[19]
    for row in v:
        d = {}
        if len(k) == len(row):
            i = 0
            for col in row:
                d[k[i]] = col
                i += 1
            tab.append(d)
        elif colname <> None and len(colname) == len(row):
            i = 0
            for col in row:
                d[colname[i]] = col
                i += 1
            tab.append(d)
        else:
            i = 1
            for col in row:
                d['col%s' % i] = col
                i += 1
            tab.append(d)
            
    now = int(time.time())
    timeArray = time.localtime(now)
    hhmmss =  time.strftime("%H:%M:%S", timeArray)
    jsn = {}
    jsn['timestamp'] = hhmmss
    jsn['tabdata'] = tab
    
    a = json.dumps(jsn,indent = 2,ensure_ascii=False)
    return a

def get_now():
    return  time.strftime("%Y%m%d%H%M%S", time.localtime(int(time.time())))

def query_excel(xlsfile,page = 1):
    xls = xlrd.open_workbook(xlsfile)
    sheet = xls.sheets()[page - 1]
    tab = []
    for i in range(sheet.nrows):
        row = []
        for cell in sheet.row_values(i):
            row.append(cell.encode('utf8'))
        tab.append(row)
    return tab



