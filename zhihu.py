import urllib
import http.cookiejar
import re
import json

'''

Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip, deflate, sdch
Accept-Language:zh-CN,zh;q=0.8
Cache-Control:max-age=0
Connection:keep-alive
Host:www.zhihu.com
Referer:http://www.zhihu.com/
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36

_xsrf:ac17f063336634b5e58d7d9a86d4b3cf
password:demo
captcha:af8z
remember_me:true
email:fuck
'''
Header = [
          ("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"),
          ("Accept-Language","zh-CN,zh;q=0.8"),
          ("Cache-Control","max-age=0"),
          ("Connection","keep-alive"),
          ("Host","www.zhihu.com"),
          ("Referer","http://www.zhihu.com/"),
          ("Upgrade-Insecure-Requests",1),
          ("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36")
          ]
captcha = 'https://www.zhihu.com/captcha.gif'

class ZhiHu:
    def __init__(self):
        cookie = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
        
    def parse_res(self, res):
        regr = re.compile(r'name="_xsrf" value=("[\d\w]+")')
        xsrfs = re.findall(regr, res)
        rnow = re.compile(r'"now":([\d]+)')
        now = re.findall(rnow, res)
#         print(now)
        captUrl = captcha + '?r='+ str(now[0])
        captResp = self.opener.open(captUrl)
        with open('captcha.jpg', 'wb') as f:
            f.write(captResp.read())
        capt = input("input captcha:")
        email = input("input email:")
        passwd = input("input password:")
#         print(capt)
        postData = {"_xsrf":str(xsrfs[0]),
                    "password":str(passwd),
                    "captcha":str(capt),
                    "remember_me":"true",
                    "email":str(email)
                    }
        lgresp = self.opener.open('https://www.zhihu.com/login/email', urllib.parse.urlencode(postData).encode(encoding='utf_8', errors='strict'))
        result = json.loads(lgresp.read().decode("utf-8"))
        print(result)
        if int(result["r"]) == 0:
            print("login success.........")
            return True
        else:
            print("login failed!!!!!!!!!!")
            return False
#         print(lgresp.read().decode("utf-8"))
#         print("done")
    def login(self):
        self.opener.addheaders = Header
        try:
            resp = self.opener.open('http://www.zhihu.com')
            context = resp.read().decode('utf-8');
            if self.parse_res(context) == True:
                ownPage = self.opener.open('https://www.zhihu.com/#signin')
                print("own page")
                print(ownPage.read().decode('utf-8', 'ignore'))
#                 with open("mainpage.html", "wb") as f:
#                     f.write(ownPage.read())
#                     print("done....")
        except Exception as e:
            print(e)
            return False
                   
if __name__ == '__main__':
    zhihu = ZhiHu()
    zhihu.login()
        
        