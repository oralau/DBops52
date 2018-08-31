#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import subprocess
import sys
import logging
import os
import datetime as dt
from datetime import datetime
sys.path.append('/scripts/DBops52/toolkit')
from processDingDing import processDingDing
from execCommand import execCommand
from getip import GetIp
from style import style
import processOpenFalcon


class collecLog():


    def collectLog(self,sysLogFile,dbLogFile, saveLogPath):
         if round(os.path.getsize(unicode(dbLogFile, 'utf8'))/float(1024 * 1024), 2)>1000:
             logging.basicConfig(level=logging.NOTSET)
             logging.info(
                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + 'File exceeding specified size')
             sys.exit()



         execCommand().execSysCommand('sed -n  \'/%s/,$p\'   %s  >  %s' % ((datetime.today()  - dt.timedelta(days=1)).strftime("%Y-%m-%d"), dbLogFile, saveLogPath + '/' + datetime.now().strftime("%Y-%m-%d") + '_db.log'))
         subprocess.call(['hostname > %s '% (saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_dbError.log')],shell=True)
         subprocess.call(['sed -i \'s/$/%s/g\'  %s '% (':'+GetIp().get_ip_address_by_dev('eth0')+':',saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_dbError.log')],shell=True)
         subprocess.call(['echo ============================mysql错误信息============================== >> %s'%(saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_dbError.log')],shell=True)
         subprocess.call(["grep -i \'\\[ERROR\\]\' %s >> %s" % (saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_db.log',saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_dbError.log')], shell=True)
         subprocess.call(['echo ============================mysql警告信息============================== >> %s'%(saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_dbError.log')],shell=True)
         subprocess.call(['grep -i \'\\[warning\\]\' %s >> %s' % (saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d") + '_db.log', saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d") + '_dbError.log')],shell=True)



         # if os.path.exists(sysLogFile+'/messages-'+( datetime.today()  - dt.timedelta(days=1)).strftime("%Y%m%d")):
         #    subprocess.call(['sed -n  \'/%s/,$p\'   %s  >  %s' % (( datetime.today()  - dt.timedelta(days=1)).strftime("%b %d"),sysLogFile+'/messages-'+( datetime.today()  - dt.timedelta(days=1)).strftime("%Y%m%d"),saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_sys.log')],shell=True)

         if os.path.exists(sysLogFile+'/messages-'+datetime.now().strftime("%Y%m%d")):
            subprocess.call(['sed -n  \'/%s/,$p\'   %s  >  %s' % (( datetime.today()  - dt.timedelta(days=1)).strftime("%b %d"),sysLogFile+'/messages-'+( datetime.today()  - dt.timedelta(days=1)).strftime("%Y%m%d"),saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_sys.log')],shell=True)
            execCommand().execSysCommand('sed -n  \'/%s/,$p\'   %s  >>  %s' %  (datetime.now().strftime("%b %d"),sysLogFile+'/messages',saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_sys.log'))

         else :
            execCommand().execSysCommand('sed -n  \'/%s/,$p\'   %s  >>  %s' %  (( datetime.today()  - dt.timedelta(days=1)).strftime("%b %d"),sysLogFile+'/messages',saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_sys.log'))
         subprocess.call(['hostname > %s '% (saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_sysError.log')],shell=True)
         subprocess.call(['sed -i \'s/$/%s/g\'  %s '% (':'+GetIp().get_ip_address_by_dev('eth0')+':',saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_sysError.log')],shell=True)
         subprocess.call(['echo ============================centos错误信息============================= >> %s' % (saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_sysError.log')],shell=True)
         subprocess.call(["grep -iE 'warn|error' %s >> %s" % (saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_sys.log',saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_sysError.log')],shell=True )






         return execCommand().execSysCommand('cat %s'%(saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_sysError.log')),execCommand().execSysCommand('cat %s'%(saveLogPath+'/'+datetime.now().strftime("%Y-%m-%d")+'_dbError.log'))




if __name__ == '__main__':

    url='https://oapi.dingtalk.com/robot/send?access_token=e5bc7d95fec0565851ab88b6c6b2390b90671a4c019a45d22879d56441c5e4e5'

    sysMesg, dbMesg = collecLog().collectLog('/var/log', '/Data/servers/mysql/logs/error.log', '/scripts/log')


    if len(dbMesg)==3:
        dbMesg= dbMesg[0] + 'Mysql没有报错'+'\n'


    else:
        dbMesg = '\n'.join(dbMesg)
        dbMesg += '\n' + '''@刘强'''


    processDingDing().sendDingDingMessage(url,dbMesg)



    if len(sysMesg)==2:
        sysMesg= sysMesg[0] + 'Centos没有报错' + '\n'


    else:
        sysMesg= '\n'.join(sysMesg)
        sysMesg+= '\n' + '''@刘强'''


    processDingDing().sendDingDingMessage(url,sysMesg)




