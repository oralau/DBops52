#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import sys
import socket
reload(sys)
sys.setdefaultencoding('utf8')

class processDingDing():

    # 发送钉钉消息
    def sendDingDingMessage(self,url,mesg):
        req = urllib2.Request(url)
        req.add_header("Content-Type", "application/json; charset=utf-8")
        data = {
            "msgtype": "text",
            "text": {
                "content": mesg
            }
        }
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, json.dumps(data))
        return response.read()





# url='https://oapi.dingtalk.com/robot/send?access_token=e5bc7d95fec0565851ab88b6c6b2390b90671a4c019a45d22879d56441c5e4e5'
# data = {
#      "msgtype": "text",
#         "text": {
#             "content": "再试试"
#         }
#     }
#
# processDingDing().sendDingDingMessage(url,data)
