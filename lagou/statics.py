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
    st.generate_image_bar('city', '城市', '职位数', '城市')
    st.generate_image_bar('education', '学历', '数量', '教育')
    st.generate_image_bar('finance_stage', '融资阶段', '数量', '融资阶段')
    st.generate_image_bar('industry_field', '行业领域', '数量', '行业领域')
    st.generate_image_bar('work_year_low', '最低工作年限', '数量', '最低工作年限')
    st.generate_image_bar('work_year_high', '最高工作年限', '数量', '最高工作年限')
    st.generate_image_bar('job_type', '厦门职位类型', '数量', '厦门职位类型', {'city':'厦门'})
    st.generate_image_bar('job_name', '厦门c++', '数量', '厦门c++', {'city':'厦门', 'LIKE':{'field':'job_name', 'value':'C++'}})
    st.generate_image_bar('job_name', '职位名称', '数量', '职位名称', {'city':'厦门'})
    st.generate_image_bar('job_name', '厦门职位名称', '数量', '厦门职位名称', {'city':'厦门'})
    st.generate_image_bar('job_name', '厦门后端职位名称', '数量', '厦门后端职位名称', {'city':'厦门', 'job_type':0})
    st.generate_image_bar('work_year_low', '工作年限', '数量', '工作年限_3_5', {"GT":{"field":"work_year_low", "value": 3}, "LT":{"field":"work_year_high", "value": 5}})
    st.generate_image_circle('salary_low', '最低薪资')
    st.generate_image_circle('salary_low', '最高薪资')
    st.generate_image_circle('job_type', '职位类型')
#     st.generate_image_circle('job_type', '厦门职位', {'city':'厦门'})
            
            