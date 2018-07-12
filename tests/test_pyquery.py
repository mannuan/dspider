# -*- coding:utf-8 -*-

from pyquery import PyQuery
import json
import re

with open('/home/mininet/test.txt','r') as f:
    _str = f.read()
p = PyQuery(_str)
menu = {}
tab_name_list = p('#shop-tabs > h2.mod-title > a').text().split(' ')
count=0
for i in p('#shop-tabs > div').items():
    tab_name = tab_name_list[count]
    count+=1
    tab_content_list = []
    if 'shop-tab-recommend' in i.attr('class'):
        dish_recommend = {}
        for i in i('p.recommend-name > a.item').items():
            info = i.text()
            dish_recommend.setdefault(re.sub(r'[\d() ]*',r'',info), {'推荐数':re.sub(r'[^\d]*',r'',info)})
        for i in i('ul.recommend-photo > li.item').items():
            item = dish_recommend.get(i('p.name').text().strip())
            item.setdefault('价格',i('span.price').text())
            item.setdefault('图片', i('img').attr('src'))
        menu.setdefault('推荐菜',dish_recommend)
    # for j in p('a.item').items():
    #     tab_content_list.append({'标题':j.attr('title'), '链接':j.attr('href'), '图片':j('img').attr('data-src')})
    # menu.setdefault(tab_name, tab_content_list)
print(json.dumps(menu, ensure_ascii=False))