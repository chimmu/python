
#-*-coding:utf-8-*-
'''
'''
import urllib.request,http.cookiejar,re
import json
from time import sleep

class Login:
    def __init__(self, limit, timeout, users):
        self.limit = limit
        self.timeout = timeout
        self.user_idx = 0
        self.users = users
        self.total = 0
        self.concern = 0
        flag = False
        self.log = open("log.txt", "w")
        for user in users:
            self.name = user["name"]
            self.passwd = user["passwd"]
            if self.login() == False:
                print("login {0} failed".format(user["name"]))
            else:
                flag = True
                self.concern = self.get_concern_number()
                self.user_idx += 1
                break
            self.user_idx += 1
        if flag == False:
            self.log.write("init error, exit")
            exit(2)
        
    def login_next(self):
        ret = False
        while self.user_idx < len(self.users):
#             self.total = 0
            self.name = self.users[self.user_idx]["name"]
            self.passwd = self.users[self.user_idx]["passwd"]
            print("move to next user: {0}".format(self.name))
            self.user_idx += 1
            if self.login() == True:
                print("login {0} success".format(self.name))
                self.concern = self.get_concern_number() #已关注多少人
                ret = True
                break
        if self.user_idx == len(self.users):
            print("meet the end")   
        return ret

    def login(self):
        self.cookie = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
        resp=self.opener.open('https://www.baidu.com/', timeout=self.timeout)
        getapiUrl = "https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true"
        resp2=self.opener.open(getapiUrl, timeout=self.timeout)
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
            resp3=self.opener.open(baiduMainLoginUrl,data=postData, timeout=self.timeout)
##            for c in cj:
##                print(c.name,"="*6,c.value)
#             print(resp3.read().decode('utf-8'))
            res = self.opener.open('http://tieba.baidu.com/f/user/json_userinfo', timeout=self.timeout)
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
            
    def get_follower_number(self):
        url = 'http://tieba.baidu.com/home/main'
        url = 'http://tieba.baidu.com'
        content = self.opener.open(url, timeout=self.timeout).read().decode('gbk')
#         content = open('test.html', 'r').read()
#         print(content)
        idre = re.compile(r'"portrait": ("[\w\d]+")')
        bid = re.findall(idre, content)
        print("id: {0}".format(bid))
        bdid = ''
        if bid != None:
            bdid = bid[0] 
        url += '/home/main'
        params = { 'id': bdid,
                  'fr': 'userbar'
                  }
        main_page = self.opener.open(url, data = urllib.parse.urlencode(params).encode('gbk'), timeout=self.timeout)
        #@todo    
    def get_concern_number(self):
        url = 'http://tieba.baidu.com/home/main?un=' + urllib.parse.quote(self.name, encoding='gbk') + '&fr=ibaidu&ie=gbk'
        print(url)
        try:
            ctx = self.opener.open(url, timeout=self.timeout).read().decode('gbk')
        except Exception as e:
            print(e)
            return 0
        rconcern = re.compile(r'<a href="[\S]+" target="_blank">(\d)</a>')
        cerns = re.findall(rconcern, ctx)
        if cerns == None or len(cerns) == 0:
            return 0
        return int(cerns[0])
    def get_page(self, tieba, page):
        if self.total and page > self.total:
            print("total page:{0}, current: {1}".format(self.total, page))
            return None
        url = 'http://tieba.baidu.com/bawu2/platform/listMemberInfo?word=' + urllib.parse.quote(tieba, encoding='gbk') + '&pn=' + str(page);
        print(url)
        try:
            resp = self.opener.open(url, timeout=self.timeout)
            dec_resp = resp.read().decode('gbk')
            return dec_resp
        except Exception as e:
            print(e)
            return []
        
    
    def get_addrs(self, tieba, page):
        resp = self.get_page(tieba, page);
        if resp == None or len(resp) == 0:
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
            if self.total > 458:
                self.total = 458
            print("total: {0}....".format(self.total))

        return addrs
    def get_tbs(self, url): 
        try:
            person_context = self.opener.open(url, timeout=self.timeout)
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
            elif len(addrs) == 0:
                page += 1
                continue
            self.follow(addrs)
            page += 1
        print("done33333333333333333333333")
        
    def check(self):
        ret = True
        if self.concern >= self.limit:
            ret = self.login_next()
        return ret
    
    def follow(self, addrs):
            for addr in addrs:
                if self.check() == False:
                    self.log.write("check error, exit..........")
                    exit(1)
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
                try:
                    context = self.opener.open('http://tieba.baidu.com/home/post/follow', data=urllib.parse.urlencode(follow_post).encode('gbk'), timeout=self.timeout)
                    ret = context.read().decode('gbk')
                except Exception as e:
                    print(e)
                    continue
#                 print(ret)
                if ret[0] != '{':
                    print("follow {0} failed!!!!!!!!".format(urllib.parse.unquote(person, 'gbk')))
                    continue
                val = ret[ret.index(':') + 1: ret.index(',')]
                if int(val) == 0:
                    self.concern += 1
                    print("follow {0} success**********".format(urllib.parse.unquote(person, 'gbk')))
                    continue
                else:
                    print("FOLLOW {0} failed!!!!!!!!!!!!!".format(urllib.parse.unquote(person, 'gbk')))
                    continue
                sleep(self.timeout)
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
    bd = Login(int(conf["limit"]), int(conf["timeout"]), conf["users"])
    for tieba in tieba_list:
        try:
            bd.get_members(tieba)
        except Exception as e:
            print(e)
            bd.log.write("exception 244")
    bd.log.close()
    
    
 
