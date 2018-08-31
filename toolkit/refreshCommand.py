#!/usr/bin/env python
# -*- coding: utf-8 -*-

from execCommand import execCommand
import os,time
import sys
import argparse



class refreshCommand():

        def upRefreshCommand(self,args,headline,commond):



                # parser = argparse.ArgumentParser()
                # parser.add_argument('-n',type=int, default=0, help='Number of executions')
                # parser.add_argument('-i',type=int, default=1, help='internel')
               #  = parser.parse_args()

                a = execCommand()

                if(args.n==0):

                        while  True:

                                for i in range(10):
                                        if  i%10==0:
                                                print  headline

                                        print ''.join(a.execSysCommand(commond))
                                        try:
                                            time.sleep(args.i)

                                        except KeyboardInterrupt, e:

                                            raise


                else:

                        for i in range(args.n):

                                if i % 10 == 0:
                                        print  headline

                                print ''.join(a.execSysCommand(commond))
                                try:
                                    time.sleep(args.i)

                                except KeyboardInterrupt, e:

                                    raise





        def currentRefreshCommand(self,args,headline,commond):



                parser = argparse.ArgumentParser()
                parser.add_argument('-n',type=int, default=0, help='Number of executions')
                parser.add_argument('-i',type=int, default=1, help='internel')
                args = parser.parse_args()

                a = execCommand()

                if(args.n==0):

                        print  headline
                        while  True:
                                sys.stdout.write(''.join(a.execSysCommand(commond)) + '\r')
                                sys.stdout.flush()

                                try:
                                    time.sleep(args.i)

                                except KeyboardInterrupt, e:

                                    raise


                else:

                        print  headline

                        for i in range(args.n):


                                sys.stdout.write(''.join(a.execSysCommand(commond))+'\r')
                                sys.stdout.flush()
                                try:
                                    time.sleep(args.i)

                                except KeyboardInterrupt, e:

                                    raise



# 使用
# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# #! /usr/bin/python
# from execCommand import ExecCommand
# import os,time
# import sys
# import argparse
# from refreshCommand import refreshCommand
#
#
#
#
#
# parser = argparse.ArgumentParser()
# parser.add_argument('--time',default=0, help='time',action="store_true")
# parser.add_argument('--vmstat', help='vmstat',action="store_true")
# parser.add_argument('-n',type=int, default=0, help='Number of executions')
# parser.add_argument('-i',type=int, default=1, help='internel')
# args = parser.parse_args()
# a = refreshCommand()
# a = refreshCommand()
# a.currentRefreshCommand(args,'time','date')