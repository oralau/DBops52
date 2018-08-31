#!/usr/bin/env python
# -*- coding: utf-8 -*-



import re
import logging
import sys
import datetime
import os


class   getFile():



    def getFile(self,fileName):
        try:
            #print os.path.getsize(fileName)/float(1024*1024)
            f = open(fileName,"rw")
            for i in f:
                yield i.strip()


        except IOError,e:
            logging.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':'+str(e))
            raise
        finally:
            file.closed





    def getSmallFile(self,fileName) :

        try:
           # print  os.path.getsize(fileName) // (1024 *  1024)
            if os.path.getsize(fileName) // (1024 * 1024) >= 100:
                logging.warning(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + 'file over 200m')
                raise

        except os.error as oe:
            logging.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + str(oe))
            raise
        try:
            #print os.path.getsize(fileName)/float(1024*1024)
            f = open(fileName,"r")
            for i in f:
                yield i.strip()


        except IOError,e:
            logging.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':'+str(e))
            raise
        finally:
            file.closed



    def getFilterLine(self,fileName,filter) :

        try:
           # print  os.path.getsize(fileName) // (1024 *  1024)
            if os.path.getsize(fileName) // (1024 * 1024) >= 100:
                logging.warning(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + 'file over 200m')
                raise

        except os.error as  oe:
            logging.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + str(oe))
            raise

        filterFile = []
        try:
            for f in open(fileName, "rw"):

                matchObj = re.search(filter,f)
                if matchObj:
                    yield matchObj.string.strip()

        except IOError,e:
            logging.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':'+str(e))
            raise
        finally:
            file.closed



    def getSmallFilterLine(self,fileName,filter) :
            try:
                # print  os.path.getsize(fileName) // (1024 *  1024)
                if os.path.getsize(fileName) // (1024 * 1024) >= 100:
                    logging.warning(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + 'file over 200m')
                    raise

            except os.error as  oe:
                logging.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':' + str(oe))
                raise

            filterFile = []
            try:
                for f in open(fileName, "r"):

                    matchObj = re.search(filter,f)
                    if matchObj:
                        yield matchObj.string.strip()

            except IOError,e:
                logging.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':'+str(e))
                raise
            finally:
                file.closed

