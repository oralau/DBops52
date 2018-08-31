#!/usr/bin/env python
# -*- coding: utf-8 -*-


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import subprocess
import sys
import logging
import os
import argparse
import calendar
import datetime as dt
from datetime import datetime
sys.path.append('/scripts/DBops52/toolkit')
from processDingDing import processDingDing
from execCommand import execCommand
from getip import GetIp
from style import style
import processOpenFalcon


class collecLog():


    def collectLog(self,sysLogFile,dbLogFile, saveLogPath,start_date):
         if round(os.path.getsize(unicode(dbLogFile, 'utf8'))/float(1024 * 1024), 2)>1000:
             logging.basicConfig(level=logging.NOTSET)
             logging.info(
                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + 'File exceeding specified size')
             sys.exit()


         print     'sed -n  \'/%s/,$p\'   %s  | tac |sed -n \'/%s/,$p\' | tac         >  %s' % (start_date, dbLogFile, start_date,saveLogPath + '/' + start_date + '_db.log')

         execCommand().execSysCommand('sed -n  \'/%s/,$p\'   %s  | tac |sed -n \'/%s/,$p\' | tac         >  %s' % (start_date, dbLogFile, start_date,saveLogPath + '/' + start_date + '_db.log'))

         subprocess.call(['hostname > %s '% (saveLogPath+'/'+start_date+'_dbError.log')],shell=True)
         subprocess.call(['sed -i \'s/$/%s/g\'  %s '% (':'+GetIp().get_ip_address_by_dev('eth0')+':',saveLogPath+'/'+start_date+'_dbError.log')],shell=True)
         subprocess.call(['echo ============================mysql错误信息============================== >> %s'%(saveLogPath+'/'+start_date+'_dbError.log')],shell=True)
         subprocess.call(["grep -i \'\\[ERROR\\]\' %s >> %s" % (saveLogPath+'/'+start_date+'_db.log',saveLogPath+'/'+start_date+'_dbError.log')], shell=True)
         subprocess.call(['echo ============================mysql警告信息============================== >> %s'%(saveLogPath+'/'+start_date+'_dbError.log')],shell=True)
         subprocess.call(['grep -i \'\\[warning\\]\' %s >> %s' % (saveLogPath+'/'+start_date + '_db.log', saveLogPath+'/'+start_date + '_dbError.log')],shell=True)



         # if os.path.exists(sysLogFile+'/messages-'+( datetime.today()  - dt.timedelta(days=1)).strftime("%Y%m%d")):
         #    subprocess.call(['sed -n  \'/%s/,$p\'   %s  >  %s' % (( datetime.today()  - dt.timedelta(days=1)).strftime("%b %d"),sysLogFile+'/messages-'+( datetime.today()  - dt.timedelta(days=1)).strftime("%Y%m%d"),saveLogPath+'/'+start_date+'_sys.log')],shell=True)

         st = dt.datetime.strptime(start_date, '%Y-%m-%d')



         sun = calendar.SUNDAY


         print (st  +  dt.timedelta(days=7)).strftime("%Y%m%d")

         if st.weekday()==sun:
             next_sunday=(st  +  dt.timedelta(days=7)).strftime("%Y%m%d")
             print next_sunday + 'abc'

         else:

             oneday = dt.timedelta(days=1)

             while st.weekday() != sun:
                 st += oneday

             next_sunday = st.strftime('%Y%m%d')

         print   'sed -n  \'/%s/,$p\'   %s | tac |sed -n \'/%s/,$p\' | tac >>  %s' % (dt.datetime.strptime(start_date, '%Y-%m-%d').strftime("%b %d"),sysLogFile+'/messages-'+next_sunday,dt.datetime.strptime(start_date, '%Y-%m-%d').strftime("%b %d"),saveLogPath+'/'+start_date+'_sys.log')

         if os.path.exists(sysLogFile+'/messages-'+next_sunday):

            subprocess.call(['sed -n  \'/%s/,$p\'   %s | tac |sed -n \'/%s/,$p\' | tac >>  %s' % (dt.datetime.strptime(start_date, '%Y-%m-%d').strftime("%b %d"),sysLogFile+'/messages-'+next_sunday,dt.datetime.strptime(start_date, '%Y-%m-%d').strftime("%b %d"),saveLogPath+'/'+start_date+'_sys.log')],shell=True)

         else :
            print    (('sed -n  \'/%s/,$p\'   %s | tac |sed -n \'/%s/,$p\' | tac >>  %s') %  (dt.datetime.strptime(start_date, '%Y-%m-%d').strftime("%b %d"),sysLogFile+'/messages',dt.datetime.strptime(start_date, '%Y-%m-%d').strftime("%b %d"),saveLogPath+'/'+start_date+'_sys.log'))

            execCommand().execSysCommand(('sed -n  \'/%s/,$p\'   %s | tac |sed -n \'/%s/,$p\' | tac >>  %s') %  (dt.datetime.strptime(start_date, '%Y-%m-%d').strftime("%b %d"),sysLogFile+'/messages',dt.datetime.strptime(start_date, '%Y-%m-%d').strftime("%b %d"),saveLogPath+'/'+start_date+'_sys.log'))


         subprocess.call(['hostname > %s '% (saveLogPath+'/'+start_date+'_sysError.log')],shell=True)
         subprocess.call(['sed -i \'s/$/%s/g\'  %s '% (':'+GetIp().get_ip_address_by_dev('eth0')+':',saveLogPath+'/'+start_date+'_sysError.log')],shell=True)
         subprocess.call(['echo ============================centos错误信息============================= >> %s' % (saveLogPath+'/'+start_date+'_sysError.log')],shell=True)
         subprocess.call(["grep -iE 'warn|error' %s >> %s" % (saveLogPath+'/'+start_date+'_sys.log',saveLogPath+'/'+start_date+'_sysError.log')],shell=True )






         return execCommand().execSysCommand('cat %s'%(saveLogPath+'/'+start_date+'_sysError.log')),execCommand().execSysCommand('cat %s'%(saveLogPath+'/'+start_date+'_dbError.log'))




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--dblog", help="database log file")
    parser.add_argument("--syslog", help="system log file",  default='/var/log')
    parser.add_argument("--savelog", help="save output path",default='.')
    parser.add_argument("--startdate", help="log start date")
    args = parser.parse_args()




    if args.dblog == None:
        print 'please intpu the database log file'
        sys.exit()


    else:



        sysLogFile = args.syslog
        dbLogFile = args.dblog
        saveLogPath = args.savelog
        start_date = ''
        if args.startdate == None:
            start_date = datetime.today().strftime('%Y-%m-%d')



        else:
            start_date = args.startdate

        collecLog().collectLog(sysLogFile,dbLogFile, saveLogPath,start_date)





