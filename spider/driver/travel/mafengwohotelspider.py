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

fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_IMG, css_selector='div.hotel-pic > a > img', attr='src'),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div.hotel-title > div > h3 > a'),
    Field(fieldname=FieldName.SHOP_URL, css_selector='div.hotel-title > div > h3 > a', attr='href'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='div.hotel-title > div > span.hotel-rate', attr='class', regex=r'[^\d]*'),
    Field(fieldname=FieldName.SHOP_GRADE, css_selector='div.hotel-info > ul > li.rating > em'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='div.hotel-info > ul > li:nth-child(2) > a > em', regex=r'[^\d]*'),
)

def get_shop_room_all(self, _str):
    p = PyQuery(_str)
    room_list = []
    for i in p('a.item._j_booking_item').items():
        room = []
        for j in i('div').items():
            room.append(j.text())
        room_list.append(room[:-1])
    return json.dumps(room_list, ensure_ascii=False)

def get_shop_traffic(self, _str):
    p = PyQuery(_str)
    distance_list = []
    for i in p('li.clearfix.clickstat').items():
        distance_list.append(i.text().split('\n'))
    return json.dumps(distance_list, ensure_ascii=False)

def get_shop_facilities(self, _str):
    p = PyQuery(_str)
    facility_list = []
    for i in p('dl.clearfix').items():
        info_list = i.text().split('\n')
        if '酒店攻略' in info_list[0]:
            facility = {info_list[0]: ''.join(info_list[1:])}
        else:
            facility = {info_list[0]: info_list[1:]}
        facility_list.append(facility)
    return json.dumps(facility_list, ensure_ascii=False)

def get_shop_stattistics(self, _str):
    p = PyQuery(_str)
    grade_list = p('dl.hotel-score.clearfix').text().split('\n')
    comment_num_list = []
    for i in p('div.rev-tags > ul').items('li'):
        comment_num_list.append(i.text().split(' ')[1:3])
    statistics = {'grade_list': grade_list, 'comment_num_list': comment_num_list}
    return json.dumps(statistics, ensure_ascii=False)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div.container > div.hotel-intro > div.intro-hd > div.location > span', attr='title', offset=6, try_times=10, pause_time=1),
    Field(fieldname=FieldName.SHOP_ROOM_RECOMMEND_ALL, css_selector='#_j_booking_info', attr='innerHTML', filter_func=get_shop_room_all, offset=6, try_times=10, pause_time=2),
    Field(fieldname=FieldName.SHOP_TRAFFIC, css_selector='#_j_map_poi_list > div.bd', attr='innerHTML', filter_func=get_shop_traffic, offset=6, try_times=10, pause_time=1),
    Field(fieldname=FieldName.SHOP_FACILITIES, css_selector='#_j_hotel_info', attr='innerHTML', filter_func=get_shop_facilities, offset=6, try_times=10, pause_time=1),
    Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#_j_comment', attr='innerHTML', filter_func=get_shop_stattistics),
)

page_shop_1 = Page(name='马蜂窝酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#_j_hotel_list > div'),mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

page_shop_2 = Page(name='马蜂窝酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div.hotel-pic > a'),mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

class MafengwoHotelSpider(TravelDriver):

    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            self.from_page_add_data_to_data_list(page=page_shop_2, data_list=shop_data_list, pre_page=page_shop_1)
        except Exception as e:
            self.error_log(e=e)

    def get_shop_info_list(self):
        self.fast_get_page('http://www.mafengwo.cn/hotel/', is_max=True)
        time.sleep(2)
        self.until_send_text_by_css_selector(css_selector='#_j_search_input', text=self.data_region)
        self.until_send_enter_by_css_selector(css_selector='#_j_search_input')
        time.sleep(1)
        self.vertical_scroll_to()#滚动到页面底部
        self.until_click_no_next_page_by_partial_link_text(link_text='后一页', func=self.get_shop_info, pause_time=3)

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception:
            self.error_log()

