# -*- coding=utf-8 -*-

import urllib
import urllib.request
import json
import http
import http.cookiejar
import re
import os
import zlib 
import time
from urllib.parse import urlencode
import gzip
import io
from io import StringIO

TOKEN_URL = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3"
INDEX_URL = "https://www.baidu.com"
LOGIN_URL = "https://passport.baidu.com/v2/api/?login"

reg_token = re.compile("\"token\"\s+:\s+\"(\w+)\"")
bdHeaders = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding":"gzip,deflate,sdch",
                "Accept-Language":"en-US,en;q=0.8,zh;q=0.6",
                "Host":"passport.baidu.com",
                "Origin":"http://www.baidu.com",
                "Referer":"http://www.baidu.com/",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
             }
MyHeader = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Host":"passport.baidu.com",
    "Origin":"http://tieba.baidu.com",
    "Referer":"http://tieba.baidu.com/",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    }
bdData = {
            "staticpage":"https://passport.baidu.com/static/passpc-account/html/V3Jump.html",
            "token":"",
            "tpl":"mn",                               #重要,需要跟TOKEN_URL中的相同
            "username":"",
            "password":"",
          }

class bdLogin:
    def __init__(self):
        #self._cookie = http.cookiejar.LWPCookieJar()
        #self._opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self._cookie))
        self._cookie = http.cookiejar.CookieJar()
        self._opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self._cookie))
        


    def login(self, user = "", psw = ""):
        print ("User:" + user)

        self._initial()                         
        self._getToken()                         #取得token,必要

        bdData["username"] = user.encode("gbk")
        bdData["password"] = psw
        bdData["token"] = self._token

        request = urllib.request.Request(LOGIN_URL, headers = bdHeaders)
        result = self._opener.open(request, urlencode(bdData).encode("gbk"))   #登录
        # decompressed_data=zlib.decompress(result.read(), 16+zlib.MAX_WBITS)
        # print (decompressed_data)
        info = self._opener.open("http://tieba.baidu.com/f/user/json_userinfo")
        buf = io.BytesIO(info.read())
        f = gzip.GzipFile(fileobj = buf)
        print(f.read().decode("GBK"))
        result = json.loads(info.read().decode("gbk"))
        print (self._opener.open("http://tieba.baidu.com/f/user/json_userinfo").read().decode("utf-8"))
        if(result["no"] == 0): 
            print ("OK, login succes!")                                 #判断是否登录成功
            return self._opener
        else:
            print("WTF, there is something wrong...")
            return None


    def _getToken(self):
        req = urllib.request.Request(TOKEN_URL, headers = MyHeader)
        ret = self._opener.open(req )
        buf = ret.read().decode("utf-8")
        print(buf)
        self._token = reg_token.findall(buf)
        print(self._token)

    def _initial(self):
        self._opener.open(LOGIN_URL)

def mymain():
    robot = bdLogin()
    #传入用户名和密码
    for line in open("user.conf"):
        user, password = str(line).strip('\n').split(",")


if __name__ == "__main__":
    mymain()
