import psycopg2
import time


class DB:

    # this method connect with database
    def connect(self):
        self.__con = psycopg2.connect(host="your host",
                                      database='your database', user='your user',
                                      password='your password', port=5432)
        self.__cur = self.__con.cursor()

    # this method close connection
    def close(self):
        self.__con.close()

    # this method select data from database
    def get(self, table_name: str, columns: list, condition: str = None,
            order: str = None, like: list = None, group_by: str = None):

        self.connect()
        columns = ", ".join(columns)

        sql = f'''SELECT {columns} FROM {table_name};'''

        if not like:
            if condition:
                sql = f'''SELECT {columns} FROM {table_name} WHERE {condition};'''

            if order:
                sql = sql.replace(";", "")
                sql += f''' ORDER BY {order};'''

            if group_by:
                sql = sql.replace(";", "")
                sql += f''' GROUP BY {group_by};'''
        else:
            sql = f'''SELECT {columns} FROM {table_name} WHERE {like[0]} LIKE {like[1]};'''

        self.__cur.execute(sql)
        try:
            data = self.__cur.fetchall()
        except:
            data = []
            time.sleep(1)
            self.get(table_name, [columns], condition, order, like)

        self.close()
        return data

    # this method update database
    # Example: g.update("admins", ["admin_permision"], ["FALSE"], "admin_user = '@omegaab'")
    def update(self, table_name: str, columns: list, data: list, condition: str = None):

        self.connect()
        columns = " = %s, ".join(columns)

        if condition:
            sql = f'''UPDATE {table_name} SET {columns} = %s WHERE {condition};'''

        else:
            sql = f'''UPDATE {table_name} SET {columns} = %s;'''

        self.__cur.execute(sql, data)
        self.__con.commit()
        self.close()

    # this method delete data from database
    def delete(self, table_name: str, condition: str):

        self.connect()
        sql = f"DELETE FROM {table_name} WHERE {condition};"

        self.__cur.execute(sql)
        self.__con.commit()

        self.close()

    # this method insert data
    def insert(self, table_name: str, columns: list, data: list):

        self.connect()
        columns = " ,".join(columns)
        values = "%s, " * len(data)

        sql = F'''INSERT INTO {table_name} ({columns}) VALUES({values[:-2]});'''
        self.__cur.execute(sql, data)
        self.__con.commit()

        self.close()

    def drop(self, table_name):

        self.connect()
        sql = f'''DROP TABLE {table_name};'''

        self.__cur.execute(sql)
        self.__con.commit()

        self.close()

    def columns(self, table_name: str):

        self.connect()
        sql = f'''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' '''

        self.__cur.execute(sql)
        data = self.__cur.fetchall()
        self.close()

        return data

    def write(self, sql, data: list = None):

        self.connect()
        if not data:
            self.__cur.execute(sql)

        else:
            self.__cur.execute(sql, data)

        self.__con.commit()
        self.close()

