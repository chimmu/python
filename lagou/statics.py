from db import MysqlDb
import json, draw
class Statics:
    def __init__(self):
        with open('config.txt', 'r') as fd:
            conf = json.load(fd)
            self._db = MysqlDb(conf['user'], conf['password'], conf['db'], conf['host'], int(conf['port'])).set_table(conf['table'])
    def generate_image_bar(self, field, xname, yname, title, condDict=None):
        res = self._db.query_group_count(field, condDict)
        labels = []
        weights = []
        for r in res:
            labels.append(r[0])
            weights.append(r[1])
        draw.draw_bar(labels, weights, xname, yname, title)
    def generate_image_circle(self, field, title, condDict=None):
        res = self._db.query_group_count(field, condDict)
        labels = []
        weights = []
        for r in res:
            labels.append(r[0])
            weights.append(r[1])
        draw.draw_circle(labels, weights, title)
if __name__ == '__main__':
    st = Statics()
#     st.generate_image_bar('city', '城市', '职位数', 'city')
#     st.generate_image_circle('city','city2')
    st.generate_image_circle('job_type','job_type', {'city':'厦门'})
            
            