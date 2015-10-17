
#-*-coding:utf-8-*-
'''
'''
import urllib.request,http.cookiejar,re
import json
from time import sleep
class Login:
    def __init__(self, name, passwd, timeout):
        self.name = name
        self.passwd = passwd
        self.total = 0
        self.timeout = timeout
    def login(self):
        self.cookie = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
        resp=self.opener.open('https://www.baidu.com/')
        getapiUrl = "https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true"
        resp2=self.opener.open(getapiUrl)
        getapiRespHtml = resp2.read().decode("utf-8")
        foundTokenVal = re.search("bdPass\.api\.params\.login_token='(?P<tokenVal>\w+)';", getapiRespHtml)
        if foundTokenVal :
            tokenVal = foundTokenVal.group("tokenVal")
            print(tokenVal)

            staticpage = "http://tieba.baidu.com/tb/static-common/html/pass/v3Jump.html"
            baiduMainLoginUrl = "https://passport.baidu.com/v2/api/?login" 
            postDict = {
                        'charset':"utf-8",
                        'token':tokenVal,
                        'isPhone':"false",
                        'index':"0",
                        'staticpage': staticpage,
                        'loginType': "1",
                        'tpl': "mn",
#                         'callback': "parent.bd__pcbs__y1km65",
                        'username': self.name,   #鐢ㄦ埛鍚�
                        'password': self.passwd,   #瀵嗙爜
                        'mem_pass':"on",
                        "apiver":"v3",
                        "logintype":"basicLogin"
                        }
            postData = urllib.parse.urlencode(postDict);
            postData = postData.encode('utf-8')
            resp3=self.opener.open(baiduMainLoginUrl,data=postData)
##            for c in cj:
##                print(c.name,"="*6,c.value)
#             print(resp3.read().decode('utf-8'))
            res = self.opener.open('http://tieba.baidu.com/f/user/json_userinfo')
            ret = res.read().decode('gbk')
#             print(ret[0])
            if ret[0] != '{':
                print("login failed")
                return False
            val = ret[ret.index(':') + 1: ret.index(',')]
            if int(val) == 0:
                print("login success")
                return True
            else:
                print("login failed" )
                return False
            
    def get_page(self, tieba, page):
        if self.total and page > self.total:
            return None
        url = 'http://tieba.baidu.com/bawu2/platform/listMemberInfo?word=' + urllib.parse.quote(tieba) + '&pn=' + str(page);
#         print(url)
        resp = self.opener.open(url)
        dec_resp = resp.read().decode('gbk')
        return dec_resp
    
    def get_addrs(self, tieba, page):
        resp = self.get_page(tieba, page);
        if resp == None:
            return resp
        pat = re.compile(r'<a href="([\w\S]*)" class="user_name"')
        res = re.findall(pat, resp)
        addrs = []
        tieba_home = 'http://tieba.baidu.com'
        for val in res:
            addrs.append(tieba_home + val) 
        if page == 1:
            pt = re.compile(r'<span class="tbui_total_page">共([\d]+)页')
            self.total = int(re.findall(pt, resp)[0])

        return addrs
    def get_tbs(self, url): 
        try:
            person_context = self.opener.open(url)
            tbs_pat = re.compile(r'PageData.tbs = "(\w+)"')
            tbs = re.findall(tbs_pat, person_context.read().decode('gbk'))
            if tbs:
#                 print("****** tbs: {0}".format(tbs[0]))
                return tbs[0]
        except Exception as e:
            print(e) 
        return None    
    
    def get_members(self, tieba):
        page = 1

        while True:
            addrs = self.get_addrs(tieba, page)
            if addrs == None:
                break
            for addr in addrs:
                print(addr)
                idx = addr.index('=') + 1;
                person = addr[idx:]
                tbs = self.get_tbs(addr)
                if tbs == None:
                    continue
                follow_post = {
                               "ie":"utf-8",
                               'un': urllib.parse.unquote(person, 'gbk'),
                               'tbs': tbs
                               }
                context = self.opener.open('http://tieba.baidu.com/home/post/follow', data=urllib.parse.urlencode(follow_post).encode('gbk'))
                ret = context.read().decode('gbk')
                print(ret)
                if ret[0] != '{':
                    print("follow {0} failed!!!!!!!!".format(person))
                    continue
                val = ret[ret.index(':') + 1: ret.index(',')]
                if int(val) == 0:
                    print("follow success**********")
                    continue
                else:
                    print("FOLLOW {0} failed!!!!!!!!!!!!!".format(person))
                    continue
                sleep(self.timeout)
            page += 1
        print("done33333333333333333333333")
        
        

def get_conf(file):
    fp = open(file, 'r')
    if fp == None:
        print("open {0} error".format(file))
        exit(1)
    conf = json.load(fp)
    fp.close() 
    return conf 

if __name__ == "__main__":
    conf = get_conf('user.txt')
    tieba_list = get_conf('tieba.txt')

    bd = Login(conf['name'], conf['passwd'], int(conf['timeout']))
    if bd.login() == False:
        exit(1)
    for tieba in tieba_list:
        bd.get_members(tieba)
    
 
