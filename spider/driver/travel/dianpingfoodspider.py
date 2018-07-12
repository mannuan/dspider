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
import random

def get_shop_tag(self, _str):
    p = PyQuery(_str)
    return json.dumps([i.text() for i in p('span').items()][1:], ensure_ascii=False)

def get_shop_rate(self, _str):
    return str(float((int(_str)/10)))

def get_shop_recommend_dish(self, _str):
    p = PyQuery(_str)
    return json.dumps([i.text() for i in p('a').items()], ensure_ascii=False)

fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='div.txt > div.tit > a > h4'),
    Field(fieldname=FieldName.SHOP_URL, css_selector='div.txt > div.tit > a', attr='href'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='div.txt > div.comment > a.review-num'),
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div.txt > div.comment > a.mean-price'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='div.txt > div.comment > span', attr='class', regex=r'[^\d]*', filter_func=get_shop_rate),
    Field(fieldname=FieldName.SHOP_TAG, css_selector='div.txt > span.comment-list', attr='innerHTML', filter_func=get_shop_tag, pause_time=1),
    Field(fieldname=FieldName.SHOP_RECOMMEND_DISH, css_selector='div.txt > div.recommend', attr='innerHTML', filter_func=get_shop_recommend_dish, pause_time=1),
)

page_shop_1 = Page(name='大众点评美食店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#shop-all-list > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

def get_shop_time(self, _str):
    return PyQuery(_str).text()

def get_shop_promotion(self, _str):
    p = PyQuery(_str)
    promotion = {}
    for i in p('div.group > div.item').items():
        info_list = i.text().split('\n')
        promotion.setdefault(info_list[0],info_list[1:])
    for i in p('div.group > a').items():
        info_list = i.text().split('\n')
        promotion.setdefault(info_list[-1],info_list[:-1])
    return json.dumps(promotion, ensure_ascii=False)

def get_shop_menu(self, _str):
    with open('/home/mininet/test.txt','w+') as f:
        f.write(_str)
    return ''

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='#address', is_focus=True, is_info=True),
    Field(fieldname=FieldName.SHOP_PHONE, css_selector='#basic-info > p', is_focus=True, is_info=True),
    Field(fieldname=FieldName.SHOP_TIME, css_selector='#basic-info > div.other.J-other.Hide > p.info.info-indent', filter_func=get_shop_time,attr='innerHTML', is_focus=True, is_info=True),
    Field(fieldname=FieldName.SHOP_PROMOTION, css_selector='#promoinfo-wrapper', attr='innerHTML', filter_func=get_shop_promotion, is_focus=True, is_info=True),
    Field(fieldname=FieldName.SHOP_MENU, css_selector='#shoptabs-wrapper', attr='innerHTML', filter_func=get_shop_menu, is_focus=True, is_info=True),
    # Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#poi-detail > div.container > div.sub-content.clearfix > div.main > div.user-comment-info', attr='innerHTML', filter_func=get_shop_statistics, is_focus=True),
)

page_shop_2 = Page(name='大众点评酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='div.hotel-info-ctn > div.hotel-info-main > h2 > a.hotel-name-link'),mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

def get_rate(self, _str):
    return str(int(re.sub('[^\d]*','',_str))/10)

def get_comment_rate_tag(self, _str):
    p = PyQuery(_str)
    tag_list = []
    for i in p('span.item').items():
        tag_list.append(i.text().strip())
    return json.dumps(tag_list, ensure_ascii=False)

def get_comment_content(self, _str):
    return PyQuery(_str).text().replace('收起评论','')

fl_comment1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_NAME, css_selector='#review-list > div.review-list-container > div.review-list-main > div.review-list-header > h1 > a', is_isolated=True),
    Field(fieldname=FieldName.COMMENT_USER_NAME, css_selector='div > div.dper-info > a'),
    Field(fieldname=FieldName.COMMENT_TIME, css_selector='div > div.misc-info.clearfix > span.time'),
    Field(fieldname=FieldName.COMMENT_USER_RATE, css_selector='div > div.dper-info > span', attr='class', filter_func=get_rate),
    Field(fieldname=FieldName.COMMENT_RATE, css_selector='div > div.review-rank > span.sml-rank-stars', attr='class', filter_func=get_rate),
    Field(fieldname=FieldName.COMMENT_RATE_TAG, css_selector='div > div.review-rank > span.score', attr='innerHTML', filter_func=get_comment_rate_tag),
    Field(fieldname=FieldName.COMMENT_CONTENT, css_selector='div > div.review-words.Hide', attr='innerHTML', filter_func=get_comment_content),
    Field(fieldname=FieldName.COMMENT_PIC_LIST, list_css_selector='div > div.review-pictures > ul', item_css_selector='li > a > img', attr='src', timeout=0),
)

page_comment_1 = Page(name='大众点评酒店评论列表', fieldlist=fl_comment1, listcssselector=ListCssSelector(list_css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.comments_collection), is_save=True)

class DianpingFoodSpider(TravelDriver):

    def more_comment(self):
        while(True):
            self.is_ready_by_proxy_ip()
            self.switch_window_by_index(index=-1)
            self.deal_with_failure_page()
            self.until_scroll_to_center_click_by_css_selector(css_selector='#comment > div > div.comment > div.more-comment > a.dp-link')
            time.sleep(2)
            self.switch_window_by_index(index=-1)  # 页面选择
            if '验证中心' in self.driver.title:
                self.info_log(data='关闭验证页面!!!')
                self.close_curr_page()
            else:
                break
        # time.sleep(1)
        # while(True):
        #     self.until_scroll_to_center_click_by_css_selector(css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-filter.clearfix > div.sort > a')
        #     time.sleep(1)
        #     self.is_ready_by_proxy_ip()
        #     self.until_scroll_to_center_click_by_css_selector(css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-filter.clearfix > div.sort-selection-list > a')
        #     time.sleep(1)
        #     self.switch_window_by_index(index=-1)
        #     if '验证' in self.driver.title:#如果是验证页面
        #         self.driver.back()
        #     else:
        #         break

    def get_shop_detail(self):
        shop_url_set = set()
        for i in Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection, host='10.1.17.15').get_collection().find(self.merge_dict(self.get_data_key(),{FieldName.SHOP_NAME:'开訫渔家'})):
            shop_url_set.add(i.get(FieldName.SHOP_URL))
        for url in shop_url_set:
            self.fast_new_page(url=url)
            self.from_fieldlist_get_data(page=page_shop_2)

    def get_shop_info_list(self):
        def get_shop_list(subtype):
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            for shop_data in shop_data_list:
                self.save_data_to_mongodb(fieldlist=fl_shop1,mongodb=Mongodb(db=TravelDriver.db,collection=TravelDriver.shop_collection, host='10.1.17.15'),data=self.merge_dict(shop_data,subtype), external_key_name=[FieldName.SUBTYPE_NAME])

        self.fast_click_first_item_page_by_partial_link_text(link_text='美食')
        time.sleep(2)
        self.until_scroll_to_center_click_by_css_selector(css_selector='#J_qs-btn')
        time.sleep(2)
        subtype_list = []
        for i in self.until_presence_of_all_elements_located_by_css_selector(css_selector='#classfy > a'):
            if i.text and i.text != '更多':
                subtype_list.append({FieldName.SUBTYPE_NAME:i.text,FieldName.SUBTYPE_URL:i.get_attribute('href')})
        for subtype in subtype_list:
            self.fast_new_page(url=subtype.get(FieldName.SUBTYPE_URL))
            self.until_click_no_next_page_by_partial_link_text(NextPageLinkTextSetup(link_text='下一页',is_proxy=False, main_pagefunc=PageFunc(get_shop_list, subtype=subtype)))
            self.close_curr_page()

    def login(self):
        self.fast_get_page(url='https://www.baidu.com')
        time.sleep(2)
        self.until_scroll_to_center_send_text_by_css_selector(css_selector='#kw', text=self.data_region + self.data_website)
        self.until_scroll_to_center_send_enter_by_css_selector(css_selector='#kw')
        self.fast_click_first_item_page_by_partial_link_text(link_text=self.data_website)
        with open('./cookies/dianping_cookies.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        for cookie in listCookies:
            self.driver.add_cookie(cookie)
        self.close_curr_page()
        self.fast_click_first_item_page_by_partial_link_text(link_text=self.data_website)

    def run_spider(self):
        try:
            self.login()
            # self.get_shop_info_list()
            self.get_shop_detail()
        except Exception as e:
            self.error_log(e=str(e))