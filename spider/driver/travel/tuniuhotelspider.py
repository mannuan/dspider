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
    Field(fieldname=FieldName.SHOP_IMG, css_selector='div.hotel-logo > img', attr='src'),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div.hotel-info > div.nameAndIcon > a'),
    Field(fieldname=FieldName.SHOP_URL, css_selector='div.hotel-info > div.nameAndIcon > a', attr='href'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='div.hotel-info.fl > div.nameAndIcon > div', attr='class', regex=r'[^\d]*'),
    Field(fieldname=FieldName.SHOP_YEAR, css_selector='div.hotel-info.fl > div.nameAndIcon > span.decorate_year'),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div.hotel-info.fl > div.addressInfo'),
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div.hotel-brief.fl > div.startPrice > span.digit'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='div.hotel-brief.fl > div.satisfaction > span.highlight'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='div.hotel-brief.fl > div.comment > a > span'),
    Field(fieldname=FieldName.SHOP_ACTIVE_STATUS, css_selector='div.hotel-brief.fl > div.lastOrderTime'),
)

def get_shop_room(self, _str):
    p = PyQuery(_str)
    room_list = []
    for i in p('div.hotel_price_list').items():
        room = {'name': i('div.fleft.s1 > div.nameDetail > p.name').text()}
        for j in i('div.fleft.s2 > div.fleft').items('span'):
            if j.text().strip():
                info_list = j.text().split('\xa0:\xa0')
                if len(info_list) == 2:
                    room.setdefault(info_list[0], info_list[1])
        for j in i('div.fleft.s2 > div.fleft > div.a2 > div').items():
            if j.text().strip():
                info_list = j.text().split('：')
                if len(info_list) == 2:
                    room.setdefault(info_list[0], info_list[1].strip().split(' '))
        type_list = []
        for j in i('div.fleft.s2 > div.item').items():
            type = j.text().split('\n')[:8]
            type_list.append(type)
        room.setdefault('type_list', type_list)
        room_list.append(room)
    return json.dumps(room_list, ensure_ascii=False)

def get_shop_traffic(self, _str):
    p = PyQuery(_str)
    type_list = p('div.detail_map > ul > li > p').text().split(' ')
    result_list = []
    for i in p('#search_result > div.cont').items():
        result_list.append(i('div.info_list').text().split('\n'))
    traffic = {}
    for i in range(len(type_list)):
        traffic.setdefault(type_list[i], result_list[i])
    return json.dumps(traffic, ensure_ascii=False)

def get_shop_statistics(self, _str):
    p = PyQuery(_str)
    grade_list = []
    for i in p('div.hotel_user_remark > div.u2 > div.k3').items('div.label'):
        grade_list.append({i('div.name').text(): i('div.score').text()})
    comment_num_list = p('div.hotel_user_remark > div.tradeoffConclude').text().split(' ')
    return json.dumps({'grade_list': grade_list, 'comment_num_list': comment_num_list}, ensure_ascii=False)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_ROOM_RECOMMEND_ALL, css_selector='#hotelPriceBody', attr='innerHTML', filter_func=get_shop_room, offset=6, try_times=10, pause_time=5),
    Field(fieldname=FieldName.SHOP_INTRO, css_selector='#hotelIntroduction > div.hotel_introduction_body'),
    Field(fieldname=FieldName.SHOP_TRAFFIC, css_selector='#hotelTraffic', attr='innerHTML', filter_func=get_shop_traffic),
    Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#hotelUserComment', attr='innerHTML', filter_func=get_shop_statistics),
)

page_shop_1 = Page(name='途牛酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#main > div.hotel-list > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

page_shop_2 = Page(name='途牛酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div.hotel-brief.fl > div.hotelDetail > a'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

class TuniuHotelSpider(TravelDriver):

    def page_shop_2_func(self):
        try:
            for i in self.until_presence_of_all_elements_located_by_css_selector(css_selector='#hotelTraffic > div.detail_map > ul > li'):
                self.until_click_by_vertical_scroll_page_down(click_ele=i)
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
        self.fast_get_page(url='http://hotel.tuniu.com/',min_time_to_wait=45,max_time_to_wait=60)
        self.focus_on_element_by_css_selector(css_selector='#txtCity')
        self.until_click_by_css_selector(css_selector='#txtCity')
        time.sleep(2)
        self.until_send_text_by_css_selector(css_selector='#txtCity', text=self.data_region)
        time.sleep(2)
        self.until_send_enter_by_css_selector(css_selector='#search_hotel')
        time.sleep(2)
        self.until_send_text_by_css_selector(css_selector='#keyWord', text=self.data_region)
        time.sleep(2)
        self.until_send_enter_by_css_selector(css_selector='#keyWord')
        self.fast_click_same_page_by_css_selector(click_css_selector='#search_hotel')
        self.vertical_scroll_to()  # 滚动到页面底部
        self.until_click_no_next_page_by_css_selector(css_selector='#main > div.pagination.clearfix > div > span.next', func=self.get_shop_info)

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception as e:
            self.error_log(e=e)
