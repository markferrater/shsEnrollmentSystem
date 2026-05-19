import pymysql

class database:
    def connect(self):
        return pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='DDC_py'
        )