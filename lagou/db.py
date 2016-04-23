import pymysql
from utils import dict2str
class MysqlDb:
    def __init__(self, User, Password, Db, Host, Port=3306):
        try:
            self._conn = pymysql.connect(host=Host, port=Port, user=User, password=Password, db=Db, charset='utf8')
        except Exception as e:
            print(e.what)
            raise e
    def set_table(self, table):
        self._table = table
        return self
    def insert(self, dataDict):
        sql = 'insert into ' + self._table 
        fields = '('
        values = '('
        for field in dataDict:
            fields += field
            fields += ','
            if isinstance(dataDict[field], str):
                values += '"' + dataDict[field] + '"'
            else:
                values += str(dataDict[field])
            values += ','
        fields = fields[0: -1]
        values = values[0:-1] 
        fields += ')'  
        values += ')'
        sql += fields + ' values ' + values + ';commit'
        print(sql)
        try:
            self._conn.query(sql)
        except Exception as e:
            print(e)
            return False
        return True
    def update(self, dataDict, condDict):
        sql = 'update ' + self._table + ' set '
    
    def query(self, fieldList, condDict=None):
        sql = 'select '
        if isinstance(fieldList, str) and fieldList == '*':
            sql += fieldList + ' from '
        elif isinstance(fieldList, list):
            for field in fieldList:
                sql += field + ',' 
            sql = sql[0:-1] + ' from '
        else:
            print('error')
            return False
        sql += self._table
        if condDict != None:
            sql += ' where ' + dict2str(condDict)
        print(sql)
        cursor = self._conn.cursor()
        cursor.execute(sql)
        return cursor
    def query_group_count(self, field, condDict=None):
        sql = 'select ' + field + ', count(*) as cnt from '
        sql += self._table
        if condDict != None:
            sql += ' where '
            for key in condDict:
                if isinstance(condDict[key], str):
                    sql += key + ' = "' + str(condDict[key]) + '" and '
                else:
                    sql += key + ' = ' + str(condDict[key]) + ' and '
            sql += ' 1 '
        sql += ' group by ' + field + ' order by cnt desc'
        print(sql)
        cursor = self._conn.cursor()
        cursor.execute(sql)
        res = []
        for c in cursor:
            res.append(c)
        return res
if __name__ == '__main__':
    db = MysqlDb('root', '123456', 'lagou', '127.0.0.1', 3306)
    db.set_table('job')
    res = db.query_group_count('city', condDict={'job_type':0})
    print(res)
