# -*- coding:utf-8 -*-

from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc
from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
from selenium import webdriver
from spider.driver.base.driver import *
import re
import time
import json
from pyquery import PyQuery
import xmltodict
#
fl_shop1 = Fieldlist(
   Field(fieldname=FieldName.SHOP_NAME,css_selector='div.sight_item_detail.clrfix > div.sight_item_about > h3 > a'),
    # 5A景区
    Field(fieldname=FieldName.SHOP_RATE, css_selector='div.sight_item_detail.clrfix > div.sight_item_about > div.sight_item_info > div.clrfix > span.level'),
    Field(fieldname=FieldName.SHOP_URL,css_selector='div.sight_item_detail.clrfix > div.sight_item_about > h3 > a',attr='href'),
    Field(fieldname=FieldName.SHOP_IMG, css_selector='div.sight_item_detail.clrfix > div.sight_item_show > div.show loading > a > img', attr='src'),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div.sight_item_detail.clrfix > div.sight_item_about > div.sight_item_info > p.address.color999 > span'),
    Field(fieldname=FieldName.SHOP_GRADE,css_selector='div.sight_item_detail.clrfix > div.sight_item_about > div.sight_item_info > div.clrfix > div.sight_item_hot > span.product_star_level > em > span'),
    #价格
    Field(fieldname=FieldName.SHOP_PRICE,css_selector='div.sight_item_detail.clrfix > div.sight_item_about > div.sight_item_pop > table > tbody > tr-nthchild:(0) > td > span.sight_item_price > em'),
    Field(fieldname=FieldName.SHOP_FEATURE, css_selector='div.sight_item_detail.clrfix > div.sight_item_about > div.sight_item_info > div.intro.color999'),
)
# print(111111111111111);
# def get_shop_service(self, _str):
#     p = PyQuery(_str)
#     service_list = []
#     for i in p('span').items():
#         service_list.append(i.text().strip())
#     return json.dumps(service_list, ensure_ascii=False)
#
# def get_shop_ticket(self, _str):
#     p = PyQuery(_str)
#     # 门票
#     p_ticket = p('#mp-tickets')
#     # 一级标题
#     for i in p_ticket('div.mp-tickettype-head').items():
#         if not i.attr('style'):  # 一级标题没有style
#             i.replace_with("<ticket class='head-level-1'>%s</ticket>" % i.text())
#     # 二级标题
#     for i in p_ticket('div.mp-tickettype-head').items():
#         if i.attr('style'):  # 一级标题有style
#             i.replace_with("<ticket class='head-level-2'>%s</ticket>" % i.text())
#     # 三级标题
#     for i in p_ticket('div.mp-tickettype').items():
#         if 'mp-tickettype-group' not in i.attr('class'):
#             info_list = i.text().split('\n')[:-1]
#             info_dict = {'名称': info_list[0], '参考门市价': info_list[1], '价格': info_list[2]}
#             i.replace_with("<ticket class='head-level-3'>%s</ticket>" % json.dumps(info_dict, ensure_ascii=False))
#     # 正文
#     for i in p_ticket('div.mp-tickettype-group').items():
#         thead_list = []
#         for j in i('mp-group-titlemain.mp-group-morepricetitle').items('mp-group-head.clrfix'):
#             thead_list.append(j.text())
#         tbody_dict_list = []
#         #有待商榷
#         for j in i('tbody').items():
#             tbody_dict = {}
#             for k in range(1, len(thead_list) + 1):
#                 tbody_dict.setdefault(thead_list[k - 1], j('td:nth-child(%s)' % k).text())
#             tbody_dict_list.append(tbody_dict)
#         i.replace_with("<ticket class='content'>%s</ticket>" % json.dumps(tbody_dict_list, ensure_ascii=False))
#     from lxml import etree
#     root = etree.Element('ticket')
#     pointer = root
#     h1 = None
#     h2 = None
#     h3 = None
#     for i in p_ticket('ticket').items():
#         if i.attr('class') == 'head-level-1':
#             pointer = root
#             pointer = etree.SubElement(pointer, 'title')
#             pointer.attrib['name'] = '%s' % i.text()
#             h1 = pointer
#         if i.attr('class') == 'head-level-2':
#             pointer = h1
#             pointer = etree.SubElement(pointer, 'title')
#             pointer.attrib['name'] = '%s' % i.text()
#             h2 = pointer
#         if i.attr('class') == 'head-level-3':
#             pointer = h2
#             pointer = etree.SubElement(pointer, 'title')
#             pointer.attrib['name'] = '%s' % i.text()
#             h3 = pointer
#         if i.attr('class') == 'content':
#             pointer = etree.SubElement(pointer, 'content')
#             pointer.text = "%s" % i.text()
#             pointer = h3
#     tickets = str(etree.tostring(root, pretty_print=True, encoding='utf-8'), 'utf-8')
#     tickets = json.loads(json.dumps(xmltodict.parse(tickets), ensure_ascii=False))
#     # 玩乐
#     p_activity = p('#J-Activity')
#     thead_list = []
#     for i in p_activity('thead').items('td'):
#         thead_list.append(i.text())
#     tbody_list = []
#     for i in p_activity('tbody').items('tr'):
#         tbody = {}
#         for j in range(1, len(thead_list)):
#             tbody.setdefault(thead_list[j - 1], i('td:nth-child(%s)' % j).text().strip())
#         tbody_list.append(tbody)
#     activitys = tbody_list
#     # 门票+酒店
#     p_drainage = p('#J-Drainage')
#     thead_list = []
#     for i in p_drainage('thead').items('td'):
#         thead_list.append(i.text())
#     tbody_list = []
#     for i in p_drainage('tbody').items('tr'):
#         tbody = {}
#         for j in range(1, len(thead_list)):
#             tbody.setdefault(thead_list[j - 1], i('td:nth-child(%s)' % j).text().strip())
#         tbody_list.append(tbody)
#     drainages = tbody_list
#     results = {'门票': tickets, '玩乐': activitys, '门票+酒店': drainages}
#     return json.dumps(results, ensure_ascii=False)
#
# def get_shop_info(self, _str):
#     p = PyQuery(_str)
#     info_dict = {}
#
#     return json.dumps(info_dict, ensure_ascii=False)

# fl_shop2 = Fieldlist(
#     Field(fieldname=FieldName.SHOP_PRICE, css_selector='div.piao_wrap redraw > div.mp-description.pngfix > div.mp-description-detail > div.mp-description-price > span.mp-description-qunar-price > em', pause_time=3, is_focus=True, is_info=True),
#     #评论次数还要改善
#     Field(fieldname=FieldName.SHOP_TIME,css_selector="#mp-charact > div >  div.mp-charact-time > div.mp-charact-content > div.mp-charact-desc > p"),
#     Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='div.piao_wrap redraw > div.mp-description.pngfix > div.mp-description-detail > div.mp-description-comments > span.mp-description-commentCount > a', is_focus=True),
#     Field(fieldname=FieldName.SHOP_SERVICE,css_selector='#root > div > div > div > div > div:nth-child(3) > div.main-bd > div > div.brief-box.clearfix > div.brief-right > ul > li.promise',attr='innerHTML', filter_func=get_shop_service, is_focus=True),
#     Field(fieldname=FieldName.SHOP_TICKET, css_selector='div.mp-tickets',attr='innerHTML', filter_func=get_shop_ticket, is_focus=True),
#     Field(fieldname=FieldName.SHOP_INFO, css_selector='#mp-charact > div >  div.mp-charact-intro > div.mp-charact-desc > p', attr='innerHTML', filter_func=get_shop_info, is_focus=True)
# )
#


page_shop_1 = Page(name='去哪儿景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#search-list > div', item_css_selector='div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

#page_shop_2 = Page(name='去哪儿景点店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div.sight_item_detail.clrfix > div.sight_item_about >  h3 > a'), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection), is_save=True)
#
# def get_comment_user_name(self, _str):
#     return _str.split(' ')[0]
#
# def get_comment_time(self, _str):
#     return re.findall(r'([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2})',_str)[0]
#
# fl_comment1 = Fieldlist(
#     Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='span.mp-comments-username', filter_func=get_comment_user_name),
#     Field(fieldname=FieldName.COMMENT_TIME, css_selector='span.mp-comments-time', filter_func=get_comment_time),
#     Field(fieldname=FieldName.SHOP_NAME, css_selector='div.sight_item_detail.clrfix > div.sight_item_about > h3 > a', is_isolated=True),
#     Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='p.mp-comments-desc'),
#     #正则表达式问题
#     Field(fieldname=FieldName.COMMENT_SCORE, css_selector='span.mp-star-level > em > span', regex=r'[^\d.]*'),
# )
#
# page_comment_1 = Page(name='景点评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#searchResultContainer > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)

class QunarSpotSpider(TravelDriver):

    def shop_detail_page_unfold(self):
        try:
            for i in self.until_presence_of_all_elements_located_by_partial_link_text(link_text='展开', timeout=1):
                self.scroll_to_center(ele=i)
                i.click()
        except Exception:
            pass

    def get_shop_info(self):
        try:

            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            # nextpagesetup = NextPageCssSelectorSetup(css_selector='div.piao_cont.section.clrfix', stop_css_selector='div.piao_cont.section.clrfix', page=page_comment_1, pause_time=2)
            #
            # extra_pagefunc = PageFunc(func=self.get_newest_comment_data_by_css_selector, nextpagesetup=nextpagesetup)
            # self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list, pre_pagefunc = PageFunc(func=self.shop_detail_page_unfold), extra_pagefunc = extra_pagefunc)
        except Exception as e:

            self.error_log(e=str(e))
        print(111)
    def get_shop_info_list(self):
        #开启第一个页面使用fast_get_page()
        time.sleep(1)
        self.fast_get_page(url='http://piao.qunar.com/', is_scroll_to_bottom=False)
        self.until_scroll_to_center_send_text_by_css_selector(css_selector="#searchValue", text=self.data_region)
        time.sleep(3)
        self.until_scroll_to_center_click_by_css_selector(css_selector='#searchBtn')
        self.until_click_no_next_page_by_css_selector(nextpagesetup=NextPageCssSelectorSetup(css_selector='#pager-container > div > a.next', pre_pagefunc=PageFunc(func=self.driver.refresh), main_pagefunc=PageFunc(func=self.get_shop_info)))

    def run_spider(self):
        try:
            self.get_shop_info_list()
            time.sleep(1000)
        except Exception as e:
            self.error_log(e=str(e))