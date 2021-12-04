# -*- coding:utf-8 -*-
from itools import MySql,send_msg_hx
import time

def get_hxid(userid):
    sql = "select id form app.app_userinfo where userid = '%s' " % userid
    hxid = ''
    for row in MySql.sel_table(sql):
        hxid = row[0]
    if hxid == '':
        print 'err:userid not signup in hx'
    return str(hxid)

def update_status(msgid):
    sql = "update app.app_system_msg set msgstatus = 'sended' where id = '%s' " % msgid
    MySql.run_sql(sql)
    
while True:
    sql = "select id,target,msg,userid from app.app_system_msg where msgstatus = 'pending' "
    for row in MySql.sel_table(sql):
        res = ''
        if row[1] == 'all':
            print type(row[2])
            target_type = 'chatgroups'
            hxtarget = ['258424278263792048']
            res = send_msg_hx(target_type,hxtarget,row[2].encode('utf-8'))
        else:
            target_type = 'users'
            target = row[1].split(',')
            hxtarget = []
            for userid in target:
                hxtarget.append(get_hxid(userid))
            res = send_msg_hx(target_type,target,row[2].encode('utf-8'))
        if res == 'ok':
            update_status(row[0])
            print 'ok:',row[1]
        else:
            print res

    time.sleep(180)



