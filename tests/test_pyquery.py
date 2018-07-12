# -*- coding:utf-8 -*-

from pyquery import PyQuery
import json
import re

with open('/home/wjl/test.txt','r') as f:
    _str = f.read()
p = PyQuery(_str)
title_list = p('h2.mod-title > a').text().split(' ')












