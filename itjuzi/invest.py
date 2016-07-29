from bs4 import BeautifulSoup
import http.cookiejar, urllib.request, pymongo,codecs,bs4,datetime, time,draw

class Invest:
    def __init__(self, dbUrl, dbName, tableName):
        self._opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self._opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36')]
        self._db = pymongo.MongoClient("mongodb://" + dbUrl)[dbName]
        self._table = tableName
        self._page = 1
        self._maxPage = 1
    def catch(self, url):
        
        while self._page <= self._maxPage:
            rurl = url + '?page=' + str(self._page)
            print(rurl)
#             resp = codecs.open('itjuzi.html', 'r', 'utf8')
            try:
                
                resp = self._opener.open(rurl)

                soup = BeautifulSoup(resp.read().decode('utf8'), "html.parser")
                infos = soup.find_all('ul', class_='list-main-eventset')
                items = []
                for info in infos[1]:
                    item = dict()
                    if isinstance(info, bs4.element.NavigableString):
                        continue
    #                 print(info)
                    day = info.find('i', class_='cell round').span.get_text().split('.')
                    item["time"] = str(datetime.date(int(day[0]), int(day[1]), int(day[2])))
                    item["company"] = info.find('i', class_='cell maincell').span.get_text()
                    item["industry"] = info.find('span', class_='tags t-small c-gray-aset').a.get_text()
                    item["city"] = info.find('span', class_='loca c-gray-aset t-small').a.get_text()
                    item["round"] = info.find('span', class_='tag gray').get_text()
                    item["money"] = info.find('i', class_='cell fina').get_text().strip()
                    try:
                        item["investor"] = info.find('span', class_='investorset').a.get_text()
                    except:
                        item["investor"] = info.find('span', class_='c-gray').get_text()
                    items.append(item)
    #                 print(item)
    #                 print(info.p)
    #                 print(info.p.span.get_text())
    #                 print(info.i.get_text())
            except Exception as e:
                print(e)
                self._page += 1
                continue
            print(items)
            if self._page == 1:
                pages = soup.find('div', class_='ui-pagechange for-sec-bottom')
                page = pages.find_all('a', attrs = {'data-ci-pagination-page':True})
                self._maxPage = int(page[len(page) - 1].get('data-ci-pagination-page'))
            self._page += 1
            if items != None:
                self._db[self._table].insert_many(items)
            time.sleep(0.01)
#             break
            print(self._page)
            
    def generate_image_bar(self, field, xname, yname, title, condDict=None):
        res = self.query_group_count(field, condDict)
        labels = []
        weights = []
        for r in res:
            labels.append(r[0])
            weights.append(r[1])
        draw.draw_bar(labels, weights, xname, yname, title)
    def generate_image_circle(self, field, title, condDict=None):
        res = self.query_group_count(field, condDict)
        labels = []
        weights = []
        for r in res:
            labels.append(r[0])
            weights.append(r[1])
        draw.draw_circle(labels, weights, title)
    def query_group_count(self, field, condDict=None):
        match = dict()
        cond = dict()
        if condDict != None:
            for key,val in condDict.items():
                if key == 'LT':
                    for k,v in val.items():
                        if k not in match:
                            match[k] = dict()
                        match[k]['$lte'] = v
                    continue
                elif key == 'GT':
                    for k,v in val.items():
                        if k not in match:
                            match[k] = dict()
                        match[k]['$gte'] = v
                    continue 
                else:
                    match[key] = val
            cond['$match'] = match
            where = [cond, {"$group":{"_id":{field: "$" + field}, "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}]
        else:
            where = [{"$group":{"_id":{field: "$" + field}, "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}]
        cursor = self._db[self._table].aggregate(where)
        res = []
        for r in cursor:
            res.append( [r['_id'][field],r['count']])
        return res
if __name__ == '__main__':
    invest = Invest('127.0.0.1', 'itjuzi', 'invest')
    invest.generate_image_bar('city', '城市', '数量', '城市投资2015', {'GT':{'time':'2015-01-01'}, 'LT':{'time':'2016-01-01'}})
    invest.generate_image_bar('city', '城市', '数量', '城市投资2016', {'GT':{'time':'2016-01-01'}})
    invest.generate_image_bar('city', '城市', '数量', '城市投资')
    invest.generate_image_bar('round', '阶段', '数量', '融资阶段总共')
    invest.generate_image_bar('round', '阶段', '数量', '融资阶段2016', {'GT':{'time':'2016-01-01'}})

    invest.generate_image_bar('industry', '行业', '数量', '行业')
    invest.generate_image_bar('industry', '行业', '数量', '行业2016', {'GT':{'time':'2016-01-01'}})
    invest.generate_image_bar('money', '融资数额', '数量', '融资数额')
    invest.generate_image_bar('money', '融资数额', '数量', '融资数额2016', {'GT':{'time':'2016-01-01'}})
    invest.generate_image_bar('investor', '投资方', '数量', '投资方')
    invest.generate_image_bar('investor', '投资方', '数量', '投资方2016', {'GT':{'time':'2016-01-01'}})
    invest.generate_image_bar('round', '阶段', '数量', '福建融资阶段总共', {'city':'福建'})
    invest.generate_image_bar('round', '阶段', '数量', '福建融资阶段2016', {'GT':{'time':'2016-01-01'}, 'city':'福建'})
    invest.generate_image_bar('industry', '行业', '数量', '福建行业', {'city':'福建'})
    invest.generate_image_bar('industry', '行业', '数量', '福建行业2016', {'GT':{'time':'2016-01-01'}, 'city':'福建'})
    invest.generate_image_bar('money', '融资数额', '数量', '福建融资数额', {'city':'福建'})
    invest.generate_image_bar('money', '融资数额', '数量', '福建融资数额2016', {'GT':{'time':'2016-01-01'}, 'city':'福建'})
    invest.generate_image_bar('investor', '投资方', '数量', '福建投资方', {'city':'福建'})
    invest.generate_image_bar('investor', '投资方', '数量', '福建投资方2016', {'GT':{'time':'2016-01-01'}, 'city':'福建'})
    invest.generate_image_circle('company', '公司')
    invest.generate_image_circle('company', '公司2016', {'GT':{'time':'2016-01-01'}})
#     invest.catch('https://www.itjuzi.com/investevents')
#     print(datetime.date(2016, 7, 13))
