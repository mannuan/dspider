# -*- coding:utf-8 -*-

from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.page import Page
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
from spider.driver.travel.core.traveldriver import TravelDriver
import time
from pyquery import PyQuery
import json
import re

fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_IMG, css_selector='div > div.h_info_pic > a > img', attr='src'),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div > div.h_info_text > div.h_info_base > p.h_info_b1 > a', attr='title'),
    Field(fieldname=FieldName.SHOP_URL, css_selector='div > div.h_info_text > div.h_info_base > p.h_info_b1 > a', attr='href'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='div > div.h_info_text > div.h_info_base > p.h_info_b1 > b', attr='class', regex=r'[^\d]*'),
    Field(fieldname=FieldName.SHOP_GRADE, css_selector='div > div.h_info_text > div.h_info_comt', regex=r'^([\d.]*).*$', repl=r'\1'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='div > div.h_info_text > div.h_info_comt', regex=r'^[\d.]*[^\d]*([\d]*)[^\d]*$', repl=r'\1'),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div > div.h_info_text > div.h_info_base > p.h_info_b2'),
    Field(fieldname=FieldName.SHOP_ACTIVE_STATUS, css_selector='div > div.h_info_text > div.h_info_base > p.lastt_book'),
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div > div.h_info_text > div.h_info_pri', regex=r'[^\d.]*'),
)

def get_shop_room(self, _str):
    p = PyQuery(_str)
    room_list = []
    for i in p('div.hdetail_type > div.htype_list > div.htype_item').items():
        info_list = i('div.htype_info').text().split('\n')
        detail = info_list[3].split('|')
        type_list = []
        for j in i('div.htype_info_list').items('tbody > tr'):
            type = j.text()
            if '上网方式' in type:
                detail.append(type.split('\n')[-1])
            else:
                type_list.append(type.split('\n'))
        room = {'name': info_list[2], 'price': info_list[0], 'detail': detail, 'product_num': info_list[1],
                'type_list': type_list}
        room_list.append(room)
    return json.dumps(room_list, ensure_ascii=False)

def get_shop_facility(self, _str):
    p = PyQuery(_str)
    facility_list = []
    flag_list = []
    for i in p('ul.dview_icon_list').items('li'):
        if not i.attr('class'):
            flag_list.append(i.text())
    facility_list.append(flag_list)
    for i in p('div.dview_info > dl').items():
        info_list = i.text().split('\n')
        if '信用卡' not in info_list[0]:
            facility_list.append({info_list[0]: info_list[1]})
    return json.dumps(facility_list, ensure_ascii=False)

def get_shop_traffic(self, _str):
    p = PyQuery(_str)
    traffic = {}
    for i in p('div.hdetail_sider > div > div.hmap_info_item').items():
        info_list = i.text().split('\n')
        for j in info_list:
            if '下一页' in j:
                info_list.remove(j)
        traffic.setdefault(info_list[0], info_list[1:])
    return json.dumps(traffic, ensure_ascii=False)

def get_shop_statistics(self, _str):
    p = PyQuery(_str)
    statistics = {}
    grade_list = p('div.cmt_hd > div.cmt_tp > div.cmt_sylst > ul').text().split('\n')
    comment_num_list = []
    for i in p('div.cmt_hd > div.cmt_tp > div.cmt_sylst > div > a').items():
        if not i.attr('class'):
            comment_num_list.append({i('span:nth-child(1)').text(): i('span:nth-child(2)').text()})
    for i in p('div.cmt_hd > div.cmt_nav > ul > li').text().split(' '):
        comment_num_list.append({re.sub(r'[^\u4e00-\u9fa5]', '', i): re.sub(r'[^\d]', '', i)})
    return json.dumps(comment_num_list, ensure_ascii=False)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_ROOM_RECOMMEND_ALL,
          css_selector='#roomSetContainer', attr='innerHTML',
          filter_func=get_shop_room, offset=6, try_times=10, pause_time=5),
    Field(fieldname=FieldName.SHOP_FACILITIES, css_selector='#hotelContent', attr='innerHTML', filter_func=get_shop_facility),
    Field(fieldname=FieldName.SHOP_TRAFFIC, css_selector='#trafficMap', attr='innerHTML', filter_func=get_shop_traffic),
    Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#review', attr='innerHTML', filter_func=get_shop_statistics),
)

page_shop_1 = Page(name='艺龙酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#hotelContainer > div.h_list > div.h_item'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

page_shop_2 = Page(name='艺龙酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div > div.h_info_text > div.h_info_base > p.h_info_b1 > a'),mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

class ElongHotelSpider(TravelDriver):

    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            self.from_page_add_data_to_data_list(page=page_shop_2, data_list=shop_data_list, pre_page=page_shop_1)
        except Exception as e:
            self.error_log(e=e)

    def get_shop_info_list(self):
        self.fast_get_page(url='http://hotel.elong.com/')
        self.until_send_text_by_css_selector(css_selector='#domesticDiv > div > dl:nth-child(1) > dd > input', text=self.data_region)
        time.sleep(5)
        self.until_send_enter_by_css_selector(css_selector='#domesticDiv > div > dl:nth-child(1) > dd > input')
        self.vertical_scroll_to()  # 滚动到页面底部
        self.until_click_no_next_page_by_partial_link_text(link_text='下一页', func=self.get_shop_info)

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception as e:
            self.error_log(e=e)
