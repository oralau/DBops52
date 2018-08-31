#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import sys
import datetime
import os


class  setParaFile():

    def getParameters(self, fileName, filter,separator=" ",position=1):

      #  返回查找字段filter一分隔符偏移量position位置的单词,position正数向右,负数向左


        try:
            line = 0
            for f in open(fileName, "rw"):


                line += 1

                words = []

                matchObj = re.search(filter,f)
                #
                # return matchObj.string


                if matchObj:


                    words=str(matchObj.string).strip().split(separator)





                    for k,v in  enumerate(words):

                        if v.strip()==filter and k+position <= len(words)-1 and k+position >=0:

                            yield 'line:'+str(line)+' '+'  value('+filter+'):'+words[k+position].strip()




        except IOError,e:
            logging.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ':'+str(e))
            raise
        finally:
            file.closed


    def setParameters(self, fileName, filter,Replacement,separator=" ",position=1):


      with open(fileName, "r") as f1, open("%s.tmp" % fileName, "w") as f2:

          line = 0
          for f in f1:

              line += 1

              words = []

              matchObj = re.search(filter, f)
              #
              # return matchObj.string


              if matchObj:

                  words = str(matchObj.string).strip().split(separator)

                  for k, v in enumerate(words):

                      if v.strip() == filter and k + position <= len(words) - 1 and k + position >= 0:



                          yield 'line:' + str(line) + ' ' + '  previous value(' + filter + '):' + words[k + position].strip()

                          words[k + position] = ' '+Replacement+' '

                  f2.write(';'.join(words).strip()+'\n')

              else:

                  f2.write(f)

      os.rename(fileName,"%s.bak"%fileName)
      os.rename("%s.tmp"%fileName, fileName)





    def setFirstParameter(self, fileName, filter,Replacement,separator=" ",position=1):


      with open(fileName, "r") as f1, open("%s.tmp" % fileName, "w") as f2:

          line = 0
          first = 0

          for f in f1:

              line += 1

              words = []

              matchObj = re.search(filter, f)
              #
              # return matchObj.string


              if matchObj and first<1:

                  words = str(matchObj.string).strip().split(separator)

                  for k, v in enumerate(words):

                      if v.strip() == filter and k + position <= len(words) - 1 and k + position >= 0 and first<1:
                          first+=1
                          yield 'line:' + str(line) + ' ' + '  previous value(' + filter + '):' + words[k + position].strip()
                          words[k + position] = ' '+Replacement+' '
                  f2.write(';'.join(words).strip()+'\n')

              else:

                  f2.write(f)

      os.rename(fileName,"%s.bak"%fileName)
      os.rename("%s.tmp"%fileName, fileName)

