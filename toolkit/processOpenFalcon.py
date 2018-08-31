import urllib2
import time
import json
import datetime
import subprocess
import sys
import logging
from execCommand import execCommand


class processOpenFalcon():

     def sentToOpenFalcon(self,count,metric,value,step,counterType='GAUGE',tags='',url='http://127.0.0.1:1988/v1/push'):

        try:

            endpoint = execCommand().execSysCommand("/bin/hostname")[0]

            for x in range(count):
                ts = int(time.time())
                payload = [
                    {
                        "endpoint":endpoint ,
                        "metric": metric,
                        "timestamp": ts,
                        "step": step,
                        "value": value,
                        "counterType": counterType,
                        "tags": tags,
                    }
                ]

                data=json.dumps(payload)


                req=urllib2.Request(url,data)
                response=urllib2.urlopen(req)


        except Exception as e:

            logging.error('errorCode' + str(e) + ':' + datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S") )
            raise
