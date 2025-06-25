
import mysql.connector;
from mysql.connector import Error;

class MySqlHelper:
    def __init__(self, host, user, password, database):
        """初始化数据库连接信息"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection  = None
        self.cursor = None
        self.connect()

    def connect(self):
        """连接数据库"""
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database,
            )
            # self.cursor = self.connection.cursor(dictionary = True)
            print("Successfully connected to database.")
        except Error as e:
            print(f"Failed to connect to database: {e}")
    
    def query_one(self, query:str, params: tuple = None):
        """
        执行查询并返回单条数据
        :param query: 查询的sql语句
        :param params: 查询参数
        :return: 一条查询结果
        """
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        return result
        
    def query_all(self, query:str, params : tuple = None):
        """
        执行查询并返回所有数据
        :param query: 查询的sql语句
        :param params: 查询参数
        :return: 查询结果列表
        """
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result
        
    def insert(self, table, data : dict):
        """
        插入一条数据
        :param table: 表明
        :param data: 要插入的数据字典 {field : value}
        """
        fields = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({fields}) VALUES ({values})"
        self.execute(sql, tuple(data.values()))

    def update(self, table, data:dict, where: str = '1=2', where_params : tuple = None):
        """
        更新数据
        :param table: 表名
        :param data: 要更新的数据字典 {field : value}
        :param where: 更新条件
        :param where_params: 更新条件参数
        """
        set_values = ', '.join([f'{field}=%s' for field in data.keys()])
        sql = f"UPDATE {table} SET {set_values} WHERE {where}"
        params = tuple(data.values())
        if where_params:
            params += where_params
        self.execute(sql, params)

    def delete(self, table, where : str = '1=2', where_params : tuple = None):
        """
        删除数据
        :param table: 表名
        :param where: 删除条件
        :param where_params: 删除条件参数
        """
        sql = f"DELETE FROM {table} WHERE {where}"
        if where_params:
            self.execute(sql, where_params)
        else:
            self.execute(sql)
    
    def execute(self, sql, params=None):
        """
        执行sql语句
        :param sql: sql语句
        :param params: 参数
        :return: 如果是select返回查询结果，其他语句返回None
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params or ())
            if sql.strip().lower().startswith(('insert', 'update', 'delete')):
                self.connection.commit()
            result = cursor.fetchall() if sql.strip().lower().startswith('select') else None
            cursor.close()
            return result
        except Error as e:
            self.connection.rollback()
            print(f"Failed to execute: {e}")
            return None
        
    def close(self):
        """
        关闭数据库连接
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Disconnected to database")

if __name__ == "__main__":
    db_helper = MySqlHelper(host='localhost', user='root', password='password', database='study')

    # query = 'SELECT * FROM students WHERE height > %s'
    # params = (170,)
    # result = db_helper.query_one(query, params)
    # result = db_helper.execute(query, params)
    # result = db_helper.query_all(query, params)
    # print(result)

    query = 'SELECT * FROM students'
    params  = ()
    print(db_helper.query_all(query, params))

    db_helper.insert('students', {'name': 'Cindy', 'height':'158.00'})
    # db_helper.update('students', {'name':'Bob'}, 'id=%s', (6,))
    # db_helper.delete('students', 'id=%s', (6,))

    query = 'SELECT * FROM students'
    params  = ()
    print(db_helper.query_all(query, params))

    db_helper.close()

    