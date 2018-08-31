#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import subprocess
import sys
import logging



class  execCommand(object):



    def  execSysCommand(self ,cmd):

        try:

            output = subprocess.check_output([cmd], shell=True, stderr=subprocess.STDOUT)

            cmdResult = []

            if sys.getsizeof(str(output)) // (1024 * 1024) >= 50:
                logging.error('errorCode' + ':' + datetime.datetime.now().strftime
                ("%Y-%m-%d %H:%M:%S") + ':' + 'sqlResult over 50m')
                raise



            for i in output.strip().split('\n'):
                cmdResult.append(i.strip())

            return cmdResult


        except subprocess.CalledProcessError as e:

            logging.error('errorCode' + str(e.returncode) + ':' + datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S") + ':' + e.output)
            raise



    def  execMysqladminCommand(self ,cmd):

        try:

            output = subprocess.check_output([cmd], shell=True, stderr=subprocess.STDOUT)

            cmdResult = []

            if sys.getsizeof(str(output)) // (1024 * 1024) >= 50:
                logging.error('errorCode' + ':' + datetime.datetime.now().strftime
                ("%Y-%m-%d %H:%M:%S") + ':' + 'sqlResult over 50m')
                sys.exit()



            for i in output.strip().split('\n'):
                cmdResult.append(i.strip())



            if cmdResult[0].find('''Warning''') != -1:
                del cmdResult[0]

            return cmdResult


        except subprocess.CalledProcessError as e:

            logging.error('errorCode' + str(e.returncode) + ':' + datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S") + ':' + e.output)
            sys.exit()




    def execDbCommand(self, sql, conn):
        execSql = 'mysql -u%s -p%s -h%s -P%s  -e ' % (
            conn['user'], conn['password'], conn['host'], conn['port'])  + sql

        dbResult = self.execSysCommand(execSql)

        if dbResult[0].find('''Warning''') != -1:
            del dbResult[0]

        return dbResult

    def execSqlCommand(self, sql, conn):
        # for i in b.execSqlCommand('select * from mysql.user'):
        #     print i['User'] + '  ' + i['Host']
        # b.execSqlCommand('''create database yu7898''')
        # b.execSqlCommand('''use yu7898;create table test(id int)''')
        # b.execSqlCommand('''use yu7898;begin;insert into test values(1);insert into test values(2);commit''')
        # 注意有空格字符的字段只能放在select后面最后一个


        execSql = 'mysql -u%s -p%s -h%s -P%s   -e ' % (
            conn['user'], conn['password'], conn['host'], conn['port'])  + sql

        sqlResult = self.execSysCommand(execSql)

        if sys.getsizeof(str(sqlResult)) // (1024 * 1024) >= 50:
            logging.error(
                'errorCode' + ':' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + 'sqlResult over 50m')
            sys.exit()

        else:

            if sqlResult[0].find('''Warning''') != -1:
                del sqlResult[0]

            columnName = []
            column = []
            rowDict = {}
            resultSet = []


            for i in range(len(sqlResult)):
                if i == 0:
                    columnName = sqlResult[i].strip().split()

                else:

                    if len(columnName)== len(sqlResult[i].strip().split()):
                        column = sqlResult[i].strip().split()
                        rowDict = dict(zip(columnName, column))
                        resultSet.append(rowDict)
                    else:
                        lastColum = ''
                        column = []

                        colList=sqlResult[i].strip().split()

                        for j in range(len(colList)):

                            if j < len(columnName)-1:
                                column.append(colList[j])

                            else:
                                lastColum=lastColum+colList[j]+' '

                        column.append(lastColum)
                        rowDict = dict(zip(columnName, column))
                        resultSet.append(rowDict)

            return resultSet