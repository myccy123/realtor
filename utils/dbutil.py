import pymysql
from decimal import Decimal
from datetime import datetime


class MySQL:
    _ip = "47.96.81.211"
    _user = "root"
    _passwd = "123456"
    _port = 3306
    _database = "visio"

    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()

    @classmethod
    def connect(cls, ip=None, user=None, passwd=None, port=None, database=None):
        params = dict()
        params['host'] = MySQL._ip if ip is None else ip
        params['user'] = MySQL._user if user is None else user
        params['passwd'] = MySQL._passwd if passwd is None else passwd
        params['port'] = MySQL._port if port is None else int(port)
        params['db'] = MySQL._database if database is None else database
        params['charset'] = 'utf8'
        db = pymysql.connect(**params)
        ret = cls(db)
        return ret

    def run(self, sql):
        # print('excute sql:', sql, sep='\n')
        print('excute sql:', sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except pymysql.MySQLError as e:
            print(e)
            self.db.rollback()
            return False
        finally:
            self.db.close()

    def execute(self, sql):
        # print('excute sql:', sql, sep='\n')
        print('excute sql:', sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except pymysql.MySQLError as e:
            print(e)
            self.db.rollback()
            return False

    def select(self, sql, hold=False):
        try:
            self.cursor.execute(sql)
            while 1:
                row = self.cursor.fetchone()
                if row is not None:
                    yield row
                else:
                    break
        except pymysql.MySQLError as e:
            print(e)
        finally:
            if not hold:
                self.db.close()

    def count(self, sql, hold=False):
        cnt = 0
        for row in self.select(sql, hold):
            cnt += 1
        return cnt

    def close(self):
        self.db.close()
