#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import pexpect
#通过spawn类启动和控制子应用程序
child = pexpect.spawn('mysql -uroot -proot')
#将pexpect的输入输出信息写到mylog.txt文件中
child.expect('mysql>')
print child.before #打印出现系统提示符前的命令输出
print child.after  #打印出现系统提示符后的命令输出
#字符串匹配则使用sendline进行回应
# send：发送命令，不回车
# sendline：发送命令，回车
# sendcontrol：发送控制符，如：sendctrol('c')等价于‘ctrl+c'
# sendeof：发送eof
child.sendline('select * from mysql.user\\G')
print child.before
print child.after
child.expect('mysql>')
child.sendline('show master status')
print child.before
print child.after

