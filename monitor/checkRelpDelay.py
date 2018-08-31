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

class checkRelpDelay():

    def checkRelpDelay(self,localCon,RemoteCon,masterServerId):


        localBinlogSql =  ''' "show slave status\G " | grep 'Master_Log_File' | grep -v 'Relay_Master_Log_File' | awk -F ':' '{print $2}'  '''
        remoteBinlogSql ='''  "show master status\G" | grep 'File'| awk -F ':' '{print $2}'  '''

        localPositionSql = ''' "show slave status\G" |  grep   'Exec_Master_Log_Pos' | awk -F ':' '{print $2}' '''
        remotePositionSql =''' "show master status\G" | grep 'Position' |  awk -F ':' '{print $2}' '''


        slaveStatusSql= ''' "show slave status\G"  '''
        masterStatusSql= ''' "show master status\G" '''


        localBinlog=''.join(execCommand().execDbCommand(localBinlogSql, localCon)).strip()
        remoteBinlog=''.join(execCommand().execDbCommand(remoteBinlogSql,RemoteCon)).strip()



        localPosition=int(''.join(execCommand().execDbCommand(localPositionSql, localCon)).strip())
        remotePosition=int(''.join(execCommand().execDbCommand(remotePositionSql, RemoteCon)).strip())

        sysCommand='/usr/bin/pt-heartbeat -D percona -P %s   --check --host=%s --user=%s  --password=%s  --master-server-id=%s'%(localCon['port'],localCon['host'],localCon['user'],localCon['password'],masterServerId)





        slaveStatus=execCommand().execDbCommand(slaveStatusSql, localCon)
        masterStatus=execCommand().execDbCommand(masterStatusSql, RemoteCon)

        print  float(execCommand().execSysCommand(sysCommand)[0])

        #if (localBinlog!=remoteBinlog)  or (remotePosition - localPosition)>= 10000000 or float(execCommand().execSysCommand(sysCommand)[0]) > 15:

        if (localBinlog!=remoteBinlog)  or float(execCommand().execSysCommand(sysCommand)[0]) > 15:


            return -1


        else:

            return  1


if __name__ == '__main__':

    try:

        a = checkRelpDelay()

        localCon = {'user': 'root', 'password': 'root', 'host': '127.0.0.1', 'port': '40238'}
        RemoteCon = {'user': 'root', 'password': 'root', 'host': '172.30.53.51', 'port': '40238'}

        if a.checkRelpDelay(localCon,RemoteCon,'535140238')==1:
            processOpenFalcon.processOpenFalcon().sentToOpenFalcon(1, 'checkRelpDelay', 1, 60)
            logging.basicConfig(level=logging.NOTSET)
            logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + 'Replication is almost  synchronous')

        else:

            processOpenFalcon.processOpenFalcon().sentToOpenFalcon(3,'checkRelpDelay', -1, 60)
            logging.basicConfig(level=logging.NOTSET)
            logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + 'Replication delay')




    except Exception as e:
        processOpenFalcon.processOpenFalcon().sentToOpenFalcon(3, 'checkRelpDelay', -1, 60)
        logging.error('checkRelpDelay exception: ' + str(e))



