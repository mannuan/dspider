# -*- coding:utf-8 -*-

from pyquery import PyQuery
import json
import re

with open('/home/wjl/test.txt','r') as f:
    _str = f.read()
p = PyQuery(_str)
statistics_dict = dict()
everyone = dict()
for i in p('div.comment-condition.J-comment-condition.Fix > div.content > span.good.J-summary').items():
    everyone.setdefault(re.sub(r'[\d()]*','',i.text()), int(re.sub(r'[^\d]*','',i.text())))
statistics_dict.setdefault('大家认为',everyone)
evaluation = dict()
for i in p('div.comment-filter-box.clearfix.J-filter > label.filter-item').items():
    if '全部' not in i.text():
        evaluation.setdefault(re.sub(r'[\d()]*', '', i.text()), int(re.sub(r'[^\d]*', '', i.text())))
statistics_dict.setdefault('评价',evaluation)
print(json.dumps(statistics_dict, ensure_ascii=False))