#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mdb


class  executeSql():

    def execSelect(self,sql,**con):


            conn = None
            conn = mdb.connect(host=con['host'], port=int(con['port']), user=con['user'], passwd=con['password'],charset=con['charset'])  # MySQLdb模块不支持utf8mb4

            with conn:
                # 获取连接上的字典 cursor，注意获取的方法，
                # 每一个 cursor 其实都是 cursor 的子类
                cur = conn.cursor(mdb.cursors.DictCursor)
                # 执行语句不变
                cur.execute(sql)
                # 获取数据方法不变
                for row in cur:
                    yield row
                # row = cur.fetchone()
                # while row :
                #     yield row
                #     row = cur.fetchone()

    def execDml(self,sql,**con):

        conn = None
        conn = mdb.connect(host=con['host'], port=int(con['port']), user=con['user'], passwd=con['password'],charset=con['charset'])  # MySQLdb模块不支持utf8mb4
        # 使用cursor()方法获取操作游标
        cur = conn.cursor()
        # SQL 插入语句
        # cur.execute(""" CREATE TABLE IF NOT EXISTS
        #         Writers(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))  """)
        # 以下插入了5条数据
        try:
            # 执行sql语句

            for i in sql:


                cur.execute(i)
                # 提交到数据库执行
                conn.commit()

        except:
            # Rollback in case there is any error
                conn.rollback()

        # 关闭数据库连接
        finally:
                conn.close()


a = executeSql()
b = ''' host='192.168.2.175',port='3306',use='root',password='root',charset='utf8' '''
c = '''select * from back_repayment.d_funds_info'''
e=a.execSelect(c,host='192.168.2.175',port='3306',user='root',password='root',charset='utf8')
for i in e:
    print i
# a = executeSql()
# b = ''' host='192.168.2.175',port='3306',use='root',password='root',charset='utf8' '''
# c = ['create database 98ddd','use 98ddd','create table test(id int)','insert into test values(1)','insert into test values(2)']
# print a.execDml(c,host='192.168.2.175',port='3306',user='root',password='root',charset='utf8')

