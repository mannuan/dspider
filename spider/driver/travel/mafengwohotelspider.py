# -*- coding:utf-8 -*-

from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.page import Page,NextPageLinkTextSetup,PageFunc
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
from spider.driver.travel.core.traveldriver import TravelDriver
import time
from pyquery import PyQuery as pq
import json
import regex as re

def get_shop_grade(self, _str):
    p = pq(_str)
    result = {}
    for i in p('li').items():
        if '分' in i.text():
            result.setdefault('评分',float(re.sub(r'[^\d.]*','',i.text())))
        elif '评价' in i.text():
            result.setdefault('评论数',int(re.sub(r'[^\d]*','',i.text())))
        elif '游记' in i.text():
            result.setdefault('游记数', int(re.sub(r'[^\d]*','',i.text())))
    return json.dumps(result, ensure_ascii=False)


fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME,css_selector='div.hotel-title > div > h3 > a'),
    Field(fieldname=FieldName.SHOP_RATE,css_selector='div.hotel-title > div > span.hotel-rate.rate5', attr='class', regex='[^\d]*', is_info=True),
    Field(fieldname=FieldName.SHOP_INTRO, css_selector='div.hotel-info > ul', attr="innerHTML", is_debug='True', filter_func=get_shop_grade, is_info=True),
)

# fl_shop2 = Fieldlist(
#     Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div.container > div.hotel-intro > div.intro-hd > div.location > span', attr='title', offset=6, try_times=10, pause_time=1),
#     Field(fieldname=FieldName.SHOP_ROOM_RECOMMEND_ALL, css_selector='#_j_booking_info', attr='innerHTML', filter_func=get_shop_room_all, offset=6, try_times=10, pause_time=2),
#     Field(fieldname=FieldName.SHOP_TRAFFIC, css_selector='#_j_map_poi_list > div.bd', attr='innerHTML', filter_func=get_shop_traffic, offset=6, try_times=10, pause_time=1),
#     Field(fieldname=FieldName.SHOP_FACILITIES, css_selector='#_j_hotel_info', attr='innerHTML', filter_func=get_shop_facilities, offset=6, try_times=10, pause_time=1),
#     Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#_j_comment', attr='innerHTML', filter_func=get_shop_stattistics),
# )

page_shop_1 = Page(name='马蜂窝酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#_j_hotel_list > div.hotel-item'),mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

# page_shop_2 = Page(name='马蜂窝酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div.hotel-pic > a'),mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

class MafengwoHotelSpider(TravelDriver):

    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            # self.from_page_add_data_to_data_list(page=page_shop_2, data_list=shop_data_list, pre_page=page_shop_1)
        except Exception as e:
            self.error_log(e=e)

    def get_shop_info_list(self):
        self.fast_get_page('http://www.mafengwo.cn/hotel/', is_max=True)
        time.sleep(2)
        self.until_send_text_by_css_selector(css_selector='#_j_search_input', text=self.data_region)
        self.until_send_enter_by_css_selector(css_selector='#_j_search_input')
        time.sleep(1)
        self.vertical_scroll_to()#滚动到页面底部,为了使得整个页面都加载完成
        self.until_click_no_next_page_by_partial_link_text(nextpagesetup=NextPageLinkTextSetup(link_text="后一页", main_pagefunc=PageFunc(func=self.get_shop_info)))

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception as e:
            self.error_log(e=e)

