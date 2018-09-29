# -*- coding:utf-8 -*-

from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.tabsetup import TabSetup
from spider.driver.base.page import Page,NextPageCssSelectorSetup,PageFunc,NextPageLinkTextSetup
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.mongodb import Mongodb
from spider.driver.travel.core.traveldriver import TravelDriver
import time
from pyquery import PyQuery
import json
import re
fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div > div.ct-text > h3 > a', is_debug=True),

    Field(fieldname=FieldName.SHOP_URL,css_selector='div > div.ct-text > h3 > a',attr='href'),
    Field(fieldname=FieldName.SHOP_IMG, css_selector=' div > div.flt1 > a > img', attr='src'),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='div > div.ct-text > ul > li:nth-child(1) > a'),
  #  Field(fieldname=FieldName.SHOP_GRADE,css_selector='div.search_ticket_assess > span.grades > em'),
    #正则表达式不一样
    Field(fieldname=FieldName.SHOP_COMMENT_NUM,css_selector='div > div.ct-text > ul > li:nth-child(2) > a', regex=r'^[^\(]*\(([\d]+)[^\)\d]*\)$', repl=r'\1'),
    Field(fieldname=FieldName.SHOP_FEATURE, css_selector='div > ul > li:nth-child(1) > div > div.ct-text > p'),
)

def get_shop_ticket():
  print(111)
def get_shop_info():
    print(222)
fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='body > div.container > div:nth-child(6) > div.mod.mod-detail > dl:nth-child(4) > dd > div:nth-child(1) > div', pause_time=3, is_focus=True, is_info=True),
    Field(fieldname=FieldName.SHOP_TIME, css_selector='body > div.container > div:nth-child(6) > div.mod.mod-detail > dl:nth-child(5) > dd > div:nth-child(1)', is_focus=True),
    #Field(fieldname=FieldName.SHOP_SERVICE,css_selector='3) > div.main-bd > div > div.brief-box.clearfix > div.brief-right > ul > li.promise',attr='innerHTML', filter_func=get_shop_service, is_focus=True),
    #门票信息尚有问题
    Field(fieldname=FieldName.SHOP_TICKET, css_selector='body > div.container > div:nth-child(6) > div.mod.mod-detail > dl:nth-child(4) > dd > div:nth-child(1) > div',attr='innerHTML', is_focus=True),
    Field(fieldname=FieldName.SHOP_INFO, css_selector='body > div.container > div:nth-child(6) > div.mod.mod-detail > div', attr='innerHTML',is_focus=True),
)
page_shop_1 = Page(name='马蜂窝景点店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#_j_search_result_left > div:nth-child(1) > div > ul > li',), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

page_shop_2 = Page(name='马蜂窝景点店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div > div.ct-text > h3 > a'), mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection), is_save=True)

def get_comment_user_name(self, _str):
    return _str.split(' ')[0]

def get_comment_time(self, _str):
    return re.findall(r'([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2})',_str)[0]

fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector=' a.name', filter_func=get_comment_user_name),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='  div.info.clearfix > span.time', filter_func=get_comment_time),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='body > div.container > div.row.row-top > div > div.title > h1', is_isolated=True),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='p'),
    #有问题
    Field(fieldname=FieldName.COMMENT_SCORE, css_selector='span', regex=r'[^\d.]*'),
)

page_comment_1 = Page(name='马蜂窝景点评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector=' div > div._j_commentlist > div.rev-list'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)

class MafengwoSpotSpider(TravelDriver):
    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            nextpagesetup = NextPageCssSelectorSetup(
                css_selector='div._j_commentlist > div.m-pagination > a.pi.pg-next',
                stop_css_selector='div._j_commentlist > div.m-pagination > a.pi.pg-last',
                page=page_comment_1, pause_time=2)
            # extra_pagefunc = PageFunc(func=self.get_newest_comment_data_by_css_selector, nextpagesetup=nextpagesetup)
            self.from_page_add_data_to_data_list(page=page_shop_2, pre_page=page_shop_1, data_list=shop_data_list)
        except Exception as e:
            self.error_log(e=str(e))

    def get_shop_info_list(self):
        self.fast_get_page('http://www.mafengwo.cn/', is_max=False)
        time.sleep(2)
        self.until_send_text_by_css_selector(css_selector='#_j_index_search_input_all', text=self.data_region)
        self.until_send_enter_by_css_selector(css_selector='#_j_index_search_input_all')
        self.fast_click_first_item_same_page_by_partial_link_text('景点')
        self.fast_click_page_by_css_selector('#_j_mfw_search_main > div.s-nav > div > div > a:nth-child(4)')
        time.sleep(1)

        self.vertical_scroll_to()  # 滚动到页面底部
        self.until_click_no_next_page_by_partial_link_text(
            nextpagesetup=NextPageLinkTextSetup(link_text="后一页", main_pagefunc=PageFunc(func=self.get_shop_info)))

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception:
            self.error_log()

