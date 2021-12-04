import sqlite3
import win32crypt
import os


def get_cookie_from_chrome(host='.alimama.com'):
    cookie_path = os.environ['LOCALAPPDATA'] \
                  + r"\Google\Chrome\User Data\Default\Cookies"
    sql = f"""select host_key,name,encrypted_value 
              from cookies where host_key='{host}'"""
    with sqlite3.connect(cookie_path) as conn:
        cu = conn.cursor()
        cookies = {
            name: win32crypt.CryptUnprotectData(encrypted_value)[1].decode() for
            host_key, name, encrypted_value in cu.execute(sql).fetchall()}
        return cookies
