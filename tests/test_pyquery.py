# -*- coding:utf-8 -*-

from pyquery import PyQuery
import json
import re

with open('/home/mininet/题目.txt','r') as f:
    str = f.read()
p = PyQuery(str)
statistics = {}
# 点评
dianping = []
for i in p('div.comment_sumary_box>div.comment_total_score').items('span'):
    (lambda x: dianping.append(x.strip()) if x else '')(i.text())
statistics.setdefault('点评', dianping)
# 印象
impression = []
count = 0
for i in p('div.user_impress').items('a'):
    count += 1
    text = i.text()
    impression.append({(lambda x: x if x else '第一个%s' % count)(re.sub(r'[^\u4e00-\u9fa5]', '', text)): re.sub(
        r'[^\d]', '', text)})
statistics.setdefault('印象', impression)
print(json.dumps(statistics, ensure_ascii=False))










