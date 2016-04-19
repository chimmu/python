import urllib.request,urllib.parse, http.cookiejar,json
from bs4 import BeautifulSoup
from db import MysqlDb

job_attrs = {'后端开发': {'type':0, 'name':'houduankaifa'},
             '前端开发': {'type':1, 'name': 'qianduankaifa'},
             '移动开发': {'type':2, 'name': 'yidongkaifa'},
             }
class LaGou:
    def __init__(self):
        self._opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self._opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36')]
        self._pageTotal = 0
        self._currentPage = 0
        with open('config.txt', 'r') as fd:
            conf = json.load(fd)
            self._db = MysqlDb(conf['user'], conf['password'], conf['db'], conf['host'], int(conf['port'])).set_table(conf['table'])
    def get_cities(self, jobType):
        url = 'http://www.lagou.com/zhaopin/' +job_attrs[jobType]['name'] + '/?labelWords=label'
        resp = self._opener.open(url).read().decode('utf8')
        soup = BeautifulSoup(resp, 'html.parser')
        cities = soup.find_all('a', attrs={'data-lg-tj-cid': 'idnull', 'data-lg-tj-id':'8o00'})
        res = []
        for city in cities:
            addr = city.get_text()
            if addr == '全国':
                continue
            res.append(addr)
        citiesex = soup.find_all('a', attrs={'data-lg-tj-cid': 'idnull', 'data-lg-tj-id':'8q00'})
        for c in citiesex:
            res.append(c.get_text())
        return res
    def split_str2int(self, raw, splitChar,tripChar, defaultValue = -1):
        if raw == '不限':
            return (-1, -1)
        elif raw =='应届毕业生':
            return (0, -1)
        print(raw)
        if raw.find(splitChar) != -1:
            low, high = raw.split(splitChar)
            l = int(low[0: -1] if low.find(tripChar) != -1 else low)
            h = int(high[0: -1] if high.find(tripChar) != -1 else high)
        else:
            l = raw[0: raw.index(tripChar) if raw.find(tripChar) != -1 else raw]
            h = defaultValue
        return (l, h)
    def translate(self, jsData):
        res = {
               'job_id': jsData['positionId'],
               'job_name': jsData['positionName'],
               'job_type': job_attrs[jsData['positionType']]['type'],
#                'job_type': 0 if jsData['positionType'] == '后端开发' else 1,
               'job_first_type': 0 if jsData['positionFirstType'] == '技术' else 1,
               'education': jsData['education'],
               'company_id':jsData['companyId'],
               'company_full_name':jsData['companyName'],
               'company_short_name': jsData['companyShortName'],
               'company_labels': ','.join(jsData['companyLabelList']),
               'boss_name': jsData['leaderName'],
               'industry_field': jsData['industryField'],
               'finance_stage': jsData['financeStage'],
               'job_nature': jsData['jobNature'],
               'city': jsData['city'],
               'plus': 1 if jsData['plus'] == '是' else 0,
               'create_time': jsData['createTime'],
               'advantage':  jsData['positionAdvantage']
               }
        res['salary_low'], res['salary_high'] = self.split_str2int(jsData['salary'], '-', 'k', -1)
        res['work_year_low'], res['work_year_high'] = self.split_str2int(jsData['workYear'], '-', '年', -1)
        res['staffs_low'], res['staffs_high'] = self.split_str2int(jsData['companySize'], '-', '人', -1)
        return res
#         if jsData['salary'].find('-'):
#             low, high = jsData['salary'].split('-')
#             res['salary_low'] = low[0: -1]
#             res['salary_high'] = high[0: -1]
#         else:
#             res['salary_low'] = jsData['salary'][0: jsData['salary'].index('k')]
#             res['salary_high'] = -1
    def get_jobs(self, jobType = '后端开发'):
        for city in self.get_cities(jobType):
            self.get_job(city, jobType)
    def get_job(self, city, jobType):
#         url = 'http://www.lagou.com/zhaopin/houduankaifa/?labelWords=label'
#         resp = self._opener.open(url).read().decode('utf8')
#         print(resp)
#         soup = BeautifulSoup(resp, 'html.parser')
        dataUrl = 'http://www.lagou.com/jobs/positionAjax.json?px=default&city=' + urllib.parse.quote(city)
        print(dataUrl)
        postData = {'first':'true','pn':1, 'kd':jobType}
        resp = self._opener.open(dataUrl, data = urllib.parse.urlencode(postData).encode('utf8')).read().decode('utf8')
        js = json.loads(resp)
        if js['success'] == False:
            return False
        self._pageTotal = js['content']['totalPageCount']
        self._currentPage = 1
        while self._currentPage <= self._pageTotal:
            for item in js['content']['result']:
                print(item)
                self._db.insert(self.translate(item))
            self._currentPage += 1
            print('*************move to next page: %d**************' % self._currentPage)
            postData = {'first':'false','pn':self._currentPage, 'kd':jobType}
            resp = self._opener.open(dataUrl, data = urllib.parse.urlencode(postData).encode('utf8')).read().decode('utf8')
            js = json.loads(resp)
        print("doneeeeeeeee")
        
if __name__ == '__main__':
    lagou = LaGou()
    lagou.get_jobs('移动开发')
#     lagou.get_jobs('前端开发')
#     lagou.get_backends()
#     lagou.get_backend()
#     print(lagou.get_cities())
        