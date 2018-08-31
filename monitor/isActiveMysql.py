#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import datetime
import subprocess
import sys
import logging
sys.path.append('/scripts/DBops52/toolkit')
import execCommand
import processOpenFalcon


class isActiveMysql():
    def pingMysql(self):

        if  execCommand.execCommand().execMysqladminCommand('''mysqladmin -uroot -proot -h127.0.0.1 -P40238 ping''') ==['mysqld is alive']:

            return 1

        else:
            return -1




if __name__ == '__main__':




    if isActiveMysql().pingMysql()==1:
        processOpenFalcon.processOpenFalcon().sentToOpenFalcon(1,'monitor','mysqlping',1,60)

        logging.basicConfig(level=logging.NOTSET)
        logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + 'mysqlping 1')






