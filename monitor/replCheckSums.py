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



class  replCheckSums():
    def checkInstSums(self,masterConn,slaveConn):


            execCommand().execSqlCommand('''"truncate table percona.checksums"''',
                                         masterConn)
            sysCommand="/usr/bin/pt-table-checksum   --max-load Threads_running=25  --max-lag=1 --host=%s --user=%s --password=%s --port=%s  --chunk-time=0.5  --recursion-method=processlist --no-check-binlog-format --no-check-replication-filters --replicate=percona.checksums"%(masterConn['host'],masterConn['user'],masterConn['password'],masterConn['port'])

            subprocess.call([sysCommand], shell=True)
            # execCommand().execSysCommand(sysCommand)

            if  execCommand().execSqlCommand('''"select * from  percona.checksums  where this_crc != master_crc"''',slaveConn) == [] :
                return  1

            else:
                return  -1







if __name__ == '__main__':

    try:

        masterConn={'user': 'root', 'password': 'root', 'host': '172.30.53.51', 'port': '40238'}
        slaveConn = {'user': 'root', 'password': 'root', 'host': '172.30.53.52', 'port': '40238'}

        if replCheckSums().checkInstSums(masterConn,slaveConn) == 1:
            processOpenFalcon.processOpenFalcon().sentToOpenFalcon(1, 'replCheckSums', 1, 60)
            logging.basicConfig(level=logging.NOTSET)
            logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + 'Replication checksums pass')

        else:

            processOpenFalcon.processOpenFalcon().sentToOpenFalcon(3,'replCheckSums', -1, 60)
            logging.basicConfig(level=logging.NOTSET)
            logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + 'Replication checksums fail')


    except Exception as e:

        processOpenFalcon.processOpenFalcon().sentToOpenFalcon(3, 'checkRelpDelay', -1, 60)
        logging.error('Replication checksums exception: ' + str(e))