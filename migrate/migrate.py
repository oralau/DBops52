#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
sys.path.append('/scripts/DBops52/toolkit')
from getConfigFile import getConfigFile
from execCommand import execCommand


class Migrate(object):

    def migrate(self, cfg_name='config.cfg'):


        #低版本运行像高版本进行全库导出会报错Segmentation fault

        parser = argparse.ArgumentParser()
        parser.add_argument("-a", help="migrate all database", action="store_true")
        parser.add_argument("-d", help="migrate Specify databases", action="store_true")
        parser.add_argument("-dp", help="migrate Specify databases without  --events --triggers --routines", action="store_true")
        parser.add_argument("-t", help="migrate Specify tables", action="store_true")
        parser.add_argument("-p", help="print command only", action="store_true")
        args = parser.parse_args()


        file_path = getConfigFile().getStrParameter('config.cfg', 'migrate', 'file_path')
        remote_user = getConfigFile().getStrParameter('config.cfg', 'remote_connect', 'user')
        remote_password = getConfigFile().getStrParameter('config.cfg', 'remote_connect', 'password')
        remote_host = getConfigFile().getStrParameter('config.cfg', 'remote_connect', 'host')
        remote_port = getConfigFile().getStrParameter('config.cfg', 'remote_connect', 'port')
        remote_con = {'user': remote_user, 'password': remote_password, 'host': remote_host,
                      'port': remote_port}
        local_user = getConfigFile().getStrParameter('config.cfg', 'local_connect', 'user')
        local_password = getConfigFile().getStrParameter('config.cfg', 'local_connect', 'password')
        local_host = getConfigFile().getStrParameter('config.cfg', 'local_connect', 'host')
        local_port = getConfigFile().getStrParameter('config.cfg', 'local_connect', 'port')
        databases = ' '.join(getConfigFile().getListParameter('config.cfg', 'migrate', 'databases'))
        databases_sql = ''
        tables_sql = ''



        for i in getConfigFile().getListParameter('config.cfg', 'migrate', 'databases'):
            databases_sql += "  '" + i + "',"

        databases_sql = databases_sql.strip(',')

        for i in getConfigFile().getListParameter('config.cfg', 'migrate', 'tables'):
            tables_sql += "  '" + i + "',"
        tables_sql = tables_sql.strip(',')

        if args.a:
            if args.p:

               dump_cmd =('mysqldump  -h%s -P%s -u%s -p%s  --opt --default-character-set=binary --single-transaction --flush-logs --master-data=2   --all-databases --routines --triggers --events'+ "   >" + file_path + '/db' + cfg_name[
                                                                                                :-4] + '.sql')% (
                             str(remote_host), str(remote_port), str(remote_user), str(remote_password))

               print dump_cmd
               imp_cmd = ('mysql -h%s -P%s -u%s -p%s -v   <  ' + 'db' + cfg_name[
                                                                    :-4] + '.sql  ' + '1>/dev/null 2>>' + 'db' + cfg_name[
                                                                                                                 :-4] + '.log') % (
                         local_host, local_port, local_user, local_password)
               print imp_cmd



            else:

                dump_cmd = (
                           'mysqldump  -h%s -P%s -u%s -p%s  --opt --default-character-set=binary --single-transaction --flush-logs --master-data=2   --all-databases --routines --triggers --events' + "   >" + file_path + '/db' + cfg_name[
                                                                                                                                                                                                                                    :-4] + '.sql') % (
                               str(remote_host), str(remote_port), str(remote_user), str(remote_password))

                print dump_cmd

                execCommand().execSysCommand('echo migrate begin >> ' + 'db' + cfg_name[:-4] + '.log')
                execCommand().execSysCommand(
                    'echo ' + "'" + dump_cmd + "'" + ' >> ' + 'db' + cfg_name[:-4] + '.log')
                execCommand().execSysCommand(dump_cmd)



                imp_cmd = ('mysql -h%s -P%s -u%s -p%s -v   <  ' + 'db' + cfg_name[
                                                                         :-4] + '.sql  ' + '1>/dev/null 2>>' + 'db' + cfg_name[
                                                                                                                      :-4] + '.log') % (
                              local_host, local_port, local_user, local_password)
                print imp_cmd

                check_sql = "head -1 " + file_path + '/db' + cfg_name[
                                                             :-4] + '.sql' + "|grep 'Warning: Using a password on the command line interface can be insecure'|wc -l"

                print check_sql

                if execCommand().execSysCommand(check_sql)[0] == '1':



                    del_cmd = "sed -i '1d'  " + file_path + '/db' + cfg_name[:-4] + '.sql'
                    print del_cmd
                    execCommand().execSysCommand(del_cmd)


                check_complete="tail -1 "+ file_path + '/db' + cfg_name[:-4] + '.sql' +" | grep 'Dump completed'|wc -l"
                print check_complete

                if  execCommand().execSysCommand(check_complete)[0] == '1':
                    cmd = ('mysql -h%s -P%s -u%s -p%s -v   <  ' + 'db' + cfg_name[
                                                                         :-4] + '.sql  ' + '1>/dev/null 2>>' + 'db' + cfg_name[
                                                                                                                      :-4] + '.log') % (
                              local_host, local_port, local_user, local_password)

                    print cmd
                    execCommand().execSysCommand('echo ' + "'"+imp_cmd+"'" + ' >> ' + 'db' + cfg_name[:-4] + '.log')
                    execCommand().execSysCommand(imp_cmd)
                    execCommand().execSysCommand('echo migrate successful >> ' + 'db' + cfg_name[:-4] + '.log')

                else:

                    print file_path + '/db' + cfg_name[:-4] + '.sql'+'  Error'




        if args.d:
            if args.p:
                dump_cmd = (
                           'mysqldump  -h%s -P%s -u%s -p%s  --single-transaction --master-data=2  --flush-logs --default-character-set=binary  --default-character-set=binary  --events --triggers --routines --set-gtid-purged=off   --databases  '+ databases + "   >" + file_path + '/db' + cfg_name[
                                                                                                                                                                                                                                    :-4] + '.sql') % (
                               str(remote_host), str(remote_port), str(remote_user), str(remote_password))

                print dump_cmd
                imp_cmd = ('mysql -h%s -P%s -u%s -p%s -v   <  ' + 'db' + cfg_name[
                                                                         :-4] + '.sql  ' + '1>/dev/null 2>>' + 'db' + cfg_name[
                                                                                                                      :-4] + '.log') % (
                              local_host, local_port, local_user, local_password)
                print imp_cmd


            else:


                dump_cmd = (
                               'mysqldump  -h%s -P%s -u%s -p%s  --single-transaction --master-data=2  --flush-logs --default-character-set=binary  --default-character-set=binary  --events --triggers --routines --set-gtid-purged=off   --databases  ' + databases + "   >" + file_path + '/db' + cfg_name[
                                                                                                                                                                                                                                                                                                    :-4] + '.sql') % (
                               str(remote_host), str(remote_port), str(remote_user), str(remote_password))

                print dump_cmd

                execCommand().execSysCommand('echo migrate begin >> ' + 'db' + cfg_name[:-4] + '.log')
                execCommand().execSysCommand('echo ' + "'" + dump_cmd + "'" + ' >> ' + 'db' + cfg_name[:-4] + '.log')
                execCommand().execSysCommand(dump_cmd)

                check_sql = "head -1 " + file_path + '/db' + cfg_name[
                                                             :-4] + '.sql' + "|grep 'Warning: Using a password on the command line interface can be insecure'|wc -l"

                print check_sql

                if execCommand().execSysCommand(check_sql)[0] == '1':
                    del_cmd = "sed -i '1d'  " + file_path + '/db' + cfg_name[:-4] + '.sql'
                    print del_cmd
                    execCommand().execSysCommand(del_cmd)

                check_complete = "tail -1 " + file_path + '/db' + cfg_name[
                                                                  :-4] + '.sql' + " | grep 'Dump completed'|wc -l"

                print check_complete


                if execCommand().execSysCommand(check_complete)[0] == '1':

                    imp_cmd = ('mysql -h%s -P%s -u%s -p%s -v   <  ' + 'db' + cfg_name[
                                                                             :-4] + '.sql  ' + '1>/dev/null 2>>' + 'db' + cfg_name[
                                                                                                                          :-4] + '.log') % (
                                  local_host, local_port, local_user, local_password)
                    print imp_cmd

                    execCommand().execSysCommand('echo ' + "'" + imp_cmd + "'" + ' >> ' + 'db' + cfg_name[:-4] + '.log')
                    #execCommand().execSysCommand(imp_cmd)
                    execCommand().execSysCommand('echo migrate successful >> ' + 'db' + cfg_name[:-4] + '.log')

                else:
                    print file_path + '/db' + cfg_name[:-4] + '.sql' + '  Error'









        if args.dp:
            if args.p:
                dump_cmd = (
                           'mysqldump  -h%s -P%s -u%s -p%s  --single-transaction --master-data=2  --flush-logs --default-character-set=binary  --default-character-set=binary   --set-gtid-purged=off   --databases  '+ databases + "   >" + file_path + '/db' + cfg_name[
                                                                                                                                                                                                                                    :-4] + '.sql') % (
                               str(remote_host), str(remote_port), str(remote_user), str(remote_password))

                print dump_cmd
                imp_cmd = ('mysql -h%s -P%s -u%s -p%s -v   <  ' + 'db' + cfg_name[
                                                                         :-4] + '.sql  ' + '1>/dev/null 2>>' + 'db' + cfg_name[
                                                                                                                      :-4] + '.log') % (
                              local_host, local_port, local_user, local_password)
                print imp_cmd


            else:


                dump_cmd = (
                               'mysqldump  -h%s -P%s -u%s -p%s  --single-transaction --master-data=2  --flush-logs --default-character-set=binary  --default-character-set=binary  --set-gtid-purged=off   --databases  ' + databases + "   >" + file_path + '/db' + cfg_name[
                                                                                                                                                                                                                                                                                                    :-4] + '.sql') % (
                               str(remote_host), str(remote_port), str(remote_user), str(remote_password))

                print dump_cmd

                execCommand().execSysCommand('echo migrate begin >> ' + 'db' + cfg_name[:-4] + '.log')
                execCommand().execSysCommand('echo ' + "'" + dump_cmd + "'" + ' >> ' + 'db' + cfg_name[:-4] + '.log')
                execCommand().execSysCommand(dump_cmd)

                check_sql = "head -1 " + file_path + '/db' + cfg_name[
                                                             :-4] + '.sql' + "|grep 'Warning: Using a password on the command line interface can be insecure'|wc -l"

                print check_sql

                if execCommand().execSysCommand(check_sql)[0] == '1':
                    del_cmd = "sed -i '1d'  " + file_path + '/db' + cfg_name[:-4] + '.sql'
                    print del_cmd
                    execCommand().execSysCommand(del_cmd)

                check_complete = "tail -1 " + file_path + '/db' + cfg_name[
                                                                  :-4] + '.sql' + " | grep 'Dump completed'|wc -l"

                print check_complete


                if execCommand().execSysCommand(check_complete)[0] == '1':

                    imp_cmd = ('mysql -h%s -P%s -u%s -p%s -v   <  ' + 'db' + cfg_name[
                                                                             :-4] + '.sql  ' + '1>/dev/null 2>>' + 'db' + cfg_name[
                                                                                                                          :-4] + '.log') % (
                                  local_host, local_port, local_user, local_password)
                    print imp_cmd

                    execCommand().execSysCommand('echo ' + "'" + imp_cmd + "'" + ' >> ' + 'db' + cfg_name[:-4] + '.log')
                    execCommand().execSysCommand(imp_cmd)
                    execCommand().execSysCommand('echo migrate successful >> ' + 'db' + cfg_name[:-4] + '.log')

                else:
                    print file_path + '/db' + cfg_name[:-4] + '.sql' + '  Error'

        if args.t:

            if args.p:

                sql = '''  "SELECT GROUP_CONCAT(concat(' --ignore-table=',TABLE_SCHEMA,'.',TABLE_NAME) SEPARATOR '  ') as ignore_tables FROM information_schema.TABLES WHERE TABLE_SCHEMA IN ( %s ) AND TABLE_NAME NOT IN (%s)"  ''' % (
                databases_sql, tables_sql)
                ignore_tables = execCommand().execSqlCommand(sql, remote_con)
                mysql_dump = (
                             "mysqldump  -h%s -P%s -u%s -p%s  --opt --default-character-set=utf8 --single-transaction --master-data=2  --set-gtid-purged=OFF --flush-logs --databases " + databases + " " +
                             ignore_tables[0]['ignore_tables'] + "   >  " + file_path + '/db' + cfg_name[
                                                                                                :-4] + '.sql') % (
                             str(remote_host), str(remote_port), str(remote_user), str(remote_password))
                print mysql_dump





                cmd = ('mysql -h%s -P%s -u%s -p%s -v   <  ' + 'db' + cfg_name[
                                                                           :-4] + '.sql  ' + '1>/dev/null 2>>' + 'db'+cfg_name[:-4] + '.log') % (
                      local_host, local_port, local_user, local_password)
                print cmd

            else:

                sql = '''  "SELECT GROUP_CONCAT(concat(' --ignore-table=',TABLE_SCHEMA,'.',TABLE_NAME) SEPARATOR '  ') as ignore_tables FROM information_schema.TABLES WHERE TABLE_SCHEMA IN ( %s ) AND TABLE_NAME NOT IN (%s)"  ''' % (
                    databases_sql, tables_sql)
                ignore_tables = execCommand().execSqlCommand(sql, remote_con)
                mysql_dump = (
                             "mysqldump  -h%s -P%s -u%s -p%s  --opt --default-character-set=utf8 --single-transaction --master-data=2  --set-gtid-purged=OFF --flush-logs --databases " + databases + " " +
                             ignore_tables[0]['ignore_tables'] + "   >  " + file_path + '/db' + cfg_name[
                                                                                                :-4] + '.sql') % (
                             str(remote_host), str(remote_port), str(remote_user), str(remote_password))

                print mysql_dump
                execCommand().execSysCommand('echo migrate begin >> ' + 'db' + cfg_name[:-4] + '.log')
                execCommand().execSysCommand('echo '+"'"+mysql_dump+"'"+ ' >> ' + 'db' + cfg_name[:-4] + '.log')
                execCommand().execSysCommand(mysql_dump)



                check_sql = "head -1 " + file_path + '/db' + cfg_name[
                                                             :-4] + '.sql' + "|grep 'Warning: Using a password on the command line interface can be insecure'|wc -l"

                print check_sql

                if execCommand().execSysCommand(check_sql)[0] == '1':



                    del_cmd = "sed -i '1d'  " + file_path + '/db' + cfg_name[:-4] + '.sql'
                    print del_cmd
                    execCommand().execSysCommand(del_cmd)


                check_complete="tail -1 "+ file_path + '/db' + cfg_name[:-4] + '.sql' +" | grep 'Dump completed'|wc -l"

                print check_complete
                if  execCommand().execSysCommand(check_complete)[0] == '1':
                    cmd = ('mysql -h%s -P%s -u%s -p%s -v   <  ' + 'db' + cfg_name[
                                                                         :-4] + '.sql  ' + '1>/dev/null 2>>' + 'db' + cfg_name[
                                                                                                                      :-4] + '.log') % (
                              local_host, local_port, local_user, local_password)

                    print cmd
                    execCommand().execSysCommand('echo ' + "'"+cmd+"'" + ' >> ' + 'db' + cfg_name[:-4] + '.log')
                    execCommand().execSysCommand(cmd)
                    execCommand().execSysCommand('echo migrate successful >> ' + 'db' + cfg_name[:-4] + '.log')

                else:

                    print file_path + '/db' + cfg_name[:-4] + '.sql'+'  Error'


if __name__ == '__main__':

    try:
        Migrate().migrate()


    except Exception as e:

        execCommand().execSysCommand('migration exception >> ' + 'db' + cfg_name[:-4] + '.log')