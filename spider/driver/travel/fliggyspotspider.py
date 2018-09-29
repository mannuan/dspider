# -*- coding:utf-8 -*-

from spider.driver.travel.core.traveldriver import TravelDriver
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc
from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
import re
import time
import json
from pyquery import PyQuery

fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div:nth-child(2) > span'),
)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='body > div > div.rax-scrollview > div > div:nth-child(1) > div > div:nth-child(1) > span'),
)

fl_comment1 = Fieldlist(
    # Field(fieldname=FieldName.SHOP_NAME, css_selector='body > div > div.rax-scrollview > div > div:nth-child(1) > div > div:nth-child(1) > span'),
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div.rate-info > div.avatar-info > div.user-nick'),
)

page_shop_1 = Page(name='飞猪景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#tus-recycleview > div > div', item_css_selector='div', item_start=4), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=False)

page_comment_1 = Page(name='飞猪景点店铺评论列表页面', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#app > div > div.poi-rate-container > div', item_start=4), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=False)


class FliggySpotSpider(TravelDriver):
    def get_shop_info_list(self):
        self.fast_get_page(url='https://h5.m.taobao.com/trip/rx-search/travel-list/index.html?keyword=千岛湖&nav=SCENIC')
        shop_data_list = self.from_page_get_data_list(page=page_shop_1)

    def get_comment_info_list(self):
        self.fast_get_page(url='https://market.m.taobao.com/apps/market/travelticket/detail.html?wh_weex=true&scenicId=1305&gsCallback=1305')
        time.sleep(2)
        self.until_presence_of_element_located_by_css_selector(css_selector='body > div > div.rax-scrollview > div > div:nth-child(1) > div > div:nth-child(3) > div:nth-child(2)').click()
        time.sleep(100)
        # comment_data_list = self.from_page_get_data_list(page=page_comment_1)

    def run_spider(self):
        # self.get_shop_info_list()
        self.get_comment_info_list()

