#!/usr/bin/env python
# -*- coding: utf-8 -*-

def abc(*abc):
    print type(abc)
    print abc[0], abc[1],abc[2]
    for i in abc:
        print i

abc(1,2,3)
