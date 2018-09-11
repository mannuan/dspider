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
    Field(fieldname=FieldName.SHOP_NAME, css_selector='a.e_title.js_list_name', attr='title'),
    Field(fieldname=FieldName.SHOP_CURR_URL, css_selector='a.e_title.js_list_name', attr='href'),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='p.adress'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='a.level_comment.level_commentbd.js_list_usercomcount', regex=r'[^\d]*'),
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='p.item_price.js_hasprice', regex=r'[^\d]*'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='em.sort.dangci'),
    Field(fieldname=FieldName.SHOP_GRADE, css_selector='a.level_score.js_list_score > strong'),
)

def get_room_all(self, _str):
    p = PyQuery(_str)
    room_type_list = []
    for i in p('div.room-item-inner.room-item-wrapper>div>div').items('div.hotel-quote-list-ct'):
        info_list = i.text().split('\n')
        room_area_list = []
        for j in i('p.room-area > cite').items():
            room_area_list.append(j.text())
        facily_list = []
        for j in i('p.facily-list > i').items():
            facily_list.append(j.attr('title'))
        room_list = []
        for j in i('div.room-type-default.tbl-tbd.js-quote').items():
            room = [j('td.e1.js-logo > div > img').attr('alt')]
            room.extend(j.text().split('\n'))
            room_list.append(room)
        room_type = {'name': info_list[1], 'detail': {'room_area': room_area_list, 'facily_list': facily_list},
                     'room_list': room_list}
        room_type_list.append(room_type)
    return json.dumps(room_type_list, ensure_ascii=False)

def get_shop_traffic(self:TravelDriver, _str):
    p = PyQuery(_str)
    traffic_list = []
    count = 0
    for i in p('ul > li').items():
        count += 1
        traffic = {'type': i.text()}
        neighbor_list = []
        for j in p('div.traf-cont.js-trafCont:nth-child(%s)' % count).items('dl'):
            neighbor_list.append({j('dt').attr('title'): j('dd').text()})
        traffic.setdefault('neighbor_list', neighbor_list)
        traffic_list.append(traffic)
    return json.dumps(traffic_list, ensure_ascii=False)

def get_shop_facilities(self, _str):
    p = PyQuery(_str)
    facility_list = []
    for i in p('dl').items():
        info_list = i.text().split('\n')
        facility = {info_list[0]: info_list[1:]}
        facility_list.append(facility)
    return json.dumps(facility_list, ensure_ascii=False)

def get_shop_statistics(self, _str):
    p = PyQuery(_str)
    statistics = {}
    tag_list = []
    for i in p('ul').items('li'):
        tag_list.append(i.text())
    statistics.setdefault('tag_list', tag_list)
    comment_num_list = []
    for i in p('dl.rank').items('dd'):
        comment_num_list.append({re.sub(r'[^\u4e00-\u9fa5]*', '', i.text()): re.sub(r'[^\d]*', '', i.text())})
    statistics.setdefault('comment_num_list', comment_num_list)
    return json.dumps(statistics, ensure_ascii=False)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_ROOM_RECOMMEND_ALL, css_selector='div.m-room-tools-bd.js-roomtool-rooms.caculate-price', attr='innerHTML', filter_func=get_room_all, pause_time=5),
    Field(fieldname=FieldName.SHOP_TRAFFIC, css_selector='#js-neighbor', attr='innerHTML', filter_func=get_shop_traffic, pause_time=1),
    Field(fieldname=FieldName.SHOP_FACILITIES, css_selector='#descContent', attr='innerHTML', filter_func=get_shop_facilities),
    Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#comment_main > div > div.b_ugcheader > div.b_ugcfilter', attr='innerHTML', filter_func=get_shop_statistics),
)

page_shop_1 = Page(name='去哪儿酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='div.b_result_box.js_list_block.b_result_commentbox'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

page_shop_2 = Page(name='去哪儿酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='a.e_title.js_list_name'),mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

class QunarHotelSpider(TravelDriver):

    def page_shop_2_func(self):
        try:
            for i in self.until_presence_of_all_elements_located_by_partial_link_text(link_text='查看其他'):
                i.click()
        except Exception:
            self.error_log(e='找不到元素')
        try:
            for i in self.until_presence_of_all_elements_located_by_partial_link_text(link_text='展开报价'):
                i.click()
        except Exception:
            self.error_log(e='找不到元素')
        try:
            for i in self.until_presence_of_all_elements_located_by_partial_link_text(link_text='查看更多房型报价'):
                i.click()
        except Exception:
            self.error_log(e='找不到元素')
        try:
            for i in self.until_presence_of_all_elements_located_by_css_selector(css_selector='#js-trafTab > ul > li > a'):
                i.click()
        except Exception:
            self.error_log(e='找不到元素')
        time.sleep(3)

    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            self.from_page_add_data_to_data_list(page=page_shop_2, data_list=shop_data_list, pre_page=page_shop_1, page_func=self.page_shop_2_func)
        except Exception as e:
            self.error_log(e=e)

    def get_shop_info_list(self):
        self.fast_get_page('http://hotel.qunar.com/')
        time.sleep(1)
        self.until_send_text_by_css_selector(css_selector='#toCity', text=self.data_region)
        self.until_send_enter_by_css_selector(css_selector='#toCity')
        self.until_send_text_by_css_selector(css_selector='#q', text=self.data_region)
        self.fast_enter_page_by_css_selector(css_selector='#q')
        self.vertical_scroll_to()#滚动到页面底部
        self.until_click_no_next_page_by_partial_link_text(link_text='下一页', func=self.get_shop_info)

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception:
            self.error_log()