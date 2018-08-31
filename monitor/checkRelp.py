#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import subprocess
import sys
import logging
sys.path.append('/scripts/DBops52/toolkit')
from execCommand import execCommand
from style import style
import processOpenFalcon

class checkRelp():



    def  checkReplError(self,localCon,RemoteCon):

        slaveIORunningSql = ''' "show slave status\G"  | grep  'Slave_IO_Running'| grep -v 'Slave_SQL_Running_State' | awk -F ':' '{print $2}' '''
        slaveSQLRunningSql =''' "show slave status\G"  | grep  'Slave_SQL_Running'| grep -v 'Slave_SQL_Running_State' | awk -F ':' '{print $2}' '''

        lastIOErrorSql = ''' "show slave status\G"  | grep  'Last_IO_Error'  | awk -F ':' '{print $2}' '''
        lastSQLErrorSql =''' "show slave status\G"  | grep  'Last_SQL_Error' | awk -F ':' '{print $2}' '''


        slaveStatusSql = ''' "show slave status\G"  '''
        masterStatusSql = ''' "show master status\G" '''



        slaveIORunning = ''.join(execCommand().execDbCommand(slaveIORunningSql, localCon)).strip()
        slaveSQLRunning = ''.join(execCommand().execDbCommand(slaveSQLRunningSql, localCon)).strip()

        lastIOError  = ''.join(execCommand().execDbCommand(lastIOErrorSql, localCon)).strip()
        lastSQLError = ''.join(execCommand().execDbCommand(lastSQLErrorSql, localCon)).strip()




        slaveStatus = execCommand().execDbCommand(slaveStatusSql, localCon)
        masterStatus = execCommand().execDbCommand(masterStatusSql, RemoteCon)



        if slaveIORunning == 'Yes' and slaveSQLRunning  == 'Yes' and lastIOError=='' and  lastSQLError=='' :

            return 1

        else:

            return -1

            # print style().underLine("slave status: ")
            #
            # for i in slaveStatus:
            #     print i
            #
            # print style().underLine("master status: ")
            #
            # for i in masterStatus:
            #     print i







# 使用checkBinlog




if __name__ == '__main__':

    a = checkRelp()

    localCon = {'user': 'root', 'password': 'root', 'host': '127.0.0.1', 'port': '40238'}
    RemoteCon = {'user': 'root', 'password': 'root', 'host': '172.30.53.51', 'port': '40238'}

    if a.checkReplError(localCon, RemoteCon)==1:
        a=processOpenFalcon.processOpenFalcon().sentToOpenFalcon(1, 'checkRelp', 1, 60)

        logging.basicConfig(level=logging.NOTSET)
        logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + 'Replication active')

    else:

        processOpenFalcon.processOpenFalcon().sentToOpenFalcon(3,'checkRelp', -1, 60)
        logging.basicConfig(level=logging.NOTSET)
        logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + 'Replication error occurred')