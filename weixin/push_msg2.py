# -*- coding:utf-8 -*-
import sys
sys.path.append('/root/myweb')
from myweb.itools import MySql
from wetools import upload_material,upload_news,send_mpnews
import uuid

def make_articles_data(thumbid,author,title,url):
    data = """
        {
             "thumb_media_id":"%s",
             "author":"%s",
             "title":"%s",
             "content_source_url":"%s",
             "content":"<img src=\'http://mmbiz.qpic.cn/mmbiz_gif/DMUsNpn7Yxqv0u9FAWtSzVbscl63L4etPHHVEsEoW9ZMmpqgG0XPTsWlM21Xkc1iaIqDsYWaNKMmIEcJ8GgyT6A/0\'>",
             "digest":"",
             "show_cover_pic":0
         }
    """ % (thumbid,author,title,url)
    return data
#http://mmbiz.qpic.cn/mmbiz_png/aQaNWLj2BmrsT7o4yxjeib0SIR5LS42XSTYSt7EpK3SMuvC8Uxf8q5vDWZcZDwFQY2s74Y0M9Teq8b77SMSegWA/0
#http://mmbiz.qpic.cn/mmbiz_png/aQaNWLj2BmprtJPLOvpic14cUO2iaLex5VmqwCTfKo4g9peylWs9YeJR4pJiceBbB9dQgnbdBROVI2qLye04Zgxqw/0
def make_news2():
    sql = """
            SELECT a.listingid,descrition,price,CAST(bedroom AS SIGNED),CAST(toilet AS SIGNED)
            FROM app.app_listing a
            LEFT JOIN app.t99_cityname b
            ON cityname = codename
            INNER JOIN (SELECT listingid FROM app.app_listingimg GROUP BY listingid) c
            ON a.listingid = c.listingid
            WHERE datadate IN (
               SELECT MAX(datadate)  AS dt
               FROM app.app_listing
               GROUP BY cityname            
            )
            AND CAST(bedroom AS SIGNED) <> 0
            AND CAST(toilet AS SIGNED) <> 0
            ORDER BY DATE_FORMAT(datadate,'%Y-%m-%d') DESC,CAST(REPLACE(REPLACE(price,'$',''),',','') AS SIGNED) DESC
            LIMIT 5
          """
    atc = []
    for row in MySql.sel_table(sql):
        title = "[%s新盘]%s|%s房%s卫|MLS#:%s" % (row[1],row[2],row[3],row[4],row[0].upper())
        sql2 = "SELECT imgname FROM app.app_listingimg WHERE listingid = '%s' LIMIT 1" % row[0]
        imgpath = '/root/myweb/static/img/logo.png'
        for img in MySql.sel_table(sql2):
            imgname = img[0]
            imgpath = '/root/myweb/data/listings/'+imgname
            break
        thumbid = upload_material(imgpath)
        make_share(row[0])
        sql3 = """
                SELECT id
                FROM app.app_sharesite t
                WHERE dataid = '%s'
                AND userid = 'wechat'
               """ % row[0]
        urlid = MySql.sel_table(sql3).next()[0]
        atc.append(make_articles_data(thumbid,'瑞安居',title.encode('utf-8')\
                                      ,'http://www.realtoraccess.com/app/get/listing1/%s' % str(urlid)))
    data = """
        {
   "articles": [
         %s,
         %s,
         %s,
         %s,
         %s
   ]
}""" % (atc[0],atc[1],atc[2],atc[3],atc[4])
    print data
    return upload_news(data)

def make_news():
    sql = """
            SELECT * FROM 
            (SELECT id,title,articlecate,img FROM app.news_article_info
            WHERE articleid='883a3c21-2316-11e7-8ffa-f44d301c3b1b'
            ORDER BY look DESC
            LIMIT 1) t
            UNION ALL
            SELECT * FROM
            (SELECT a.id,a.title,a.articlecate,a.img FROM app.news_article_info a
            INNER JOIN
            (
            SELECT articlecate,MAX(id) AS id
            FROM app.news_article_info
            GROUP BY articlecate
            ) b
            ON a.id = b.id
            INNER JOIN(
            SELECT DISTINCT codename,sortid FROM app.t99_articletype
            ) c
            ON a.articlecate = c.codename
            ORDER BY c.sortid
            LIMIT 6) t2
          """
    atc = []
    fst = True
    for row in MySql.sel_table(sql):
        title = row[1]
        if fst:
            imgpath = '/root/myweb/data/' + row[3]
            fst = False
        else:
            imgpath = '/root/myweb/data/weixin/' + row[2] + '.png'
        thumbid = upload_material(imgpath)
        atc.append(make_articles_data(thumbid,'瑞安居',title.encode('utf-8')\
                                      ,'http://www.realtoraccess.com/news/%s' % row[0]))
    data = """
        {
   "articles": [
         %s,
         %s,
         %s,
         %s,
         %s,
         %s,
         %s
   ]
}""" % (atc[0],atc[1],atc[2],atc[3],atc[4],atc[5],atc[6])
    print data
    return upload_news(data)

def make_share(listingid):
    sql = """
            INSERT INTO app.app_sharesite VALUES
            (
            NULL,
            '%s',
            '',
            'wechat',
            '%s',
            'listing1',
            now(),
            '',
            0,
            0,
            0,
            '1',
            '1',
            'a1b1c1d1e0f0g0h0i0j0k0l0m1',
            ''
            )
          """ % (str(uuid.uuid1()),listingid)
    MySql.run_sql(sql)

def main():
    print send_mpnews(make_news2())
    
if __name__ == '__main__':
    main()


