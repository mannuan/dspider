# -*- coding:utf-8 -*-

from spider.driver.travel.core.traveldriver import *
from spider.driver.base.field import Fieldlist,Field,FieldName
from spider.driver.base.listcssselector import ListCssSelector
from spider.driver.base.tabsetup import TabSetup
from pyquery import PyQuery

fl_shop1 = Fieldlist(
    Field(fieldname=FieldName.SHOP_IMG, css_selector='a > img', attr='src'),
    Field(fieldname=FieldName.SHOP_NAME, css_selector='dl > dt > a'),
    Field(fieldname=FieldName.SHOP_URL, css_selector='dl > dt > a', attr='href'),
    Field(fieldname=FieldName.SHOP_RATE, css_selector='dl > dt > span'),
    Field(fieldname=FieldName.SHOP_CATEGORY_NAME, css_selector='dl > dd.proInfo-tips'),
    Field(fieldname=FieldName.SHOP_DISTANCE, css_selector='dl > dd.porInfo-pos'),
    Field(fieldname=FieldName.SHOP_ADDRESS, css_selector='dl > dd.proInfo-address'),
    Field(fieldname=FieldName.SHOP_PRICE, css_selector='div.priceInfo > div.priceInfo-price', regex=r'[^\d]*'),
    Field(fieldname=FieldName.SHOP_STATISFACTION_PERCENT, css_selector='div.priceInfo > div > ul.product-number', regex=r'^[^\d]*([\d.]*)[^\d]*好评.*$', repl=r'\1'),
    Field(fieldname=FieldName.SHOP_COMMENT_NUM, css_selector='div.priceInfo > div > ul.product-number', regex='^.*来自([\d]*)条点评.*$', repl=r'\1'),
)

def get_room_all(self, _str):
    p = PyQuery(_str)
    room_list = []
    for i in p('div.room_list.roomList').items():
        info_list = i('dt').text().split('\n')
        detail = info_list[1].split('|')
        detail.extend(info_list[2:])
        room = {'name': info_list[0], 'detail': detail}
        product_list = []
        for j in i('dl > dd > table > tbody > tr').items():
            product_list.append(j.text().split('\n'))
        room.setdefault('room_list', product_list)
        room_list.append(room)
    return json.dumps(room_list, ensure_ascii=False)

def get_shop_facility(self, _str):
    p = PyQuery(_str)
    facility = {}
    for i in p('dl').items():
        info_list = i.text().split('\n')
        facility.setdefault(info_list[0], info_list[1:])
    return json.dumps(facility, ensure_ascii=False)

def get_shop_traffic(self, _str):
    p = PyQuery(_str)
    info_list = p('div.jiaotong_all1').text().split('\n')
    traffic = {info_list[0]: info_list[1:]}
    return json.dumps(traffic, ensure_ascii=False)

def get_shop_statistics(self, _str):
    p = PyQuery(_str)
    percent_list = p('div.new-cominfo').text().split('\n')
    comment_num_list = p('div.comheatd > ul').text().split('\n')
    statistics = {'percent_list': percent_list, 'comment_num_list': comment_num_list}
    return json.dumps(statistics, ensure_ascii=False)

fl_shop2 = Fieldlist(
    Field(fieldname=FieldName.SHOP_ROOM_RECOMMEND_ALL, css_selector='#hotelbook', attr='innerHTML', filter_func=get_room_all, offset=6, try_times=10, pause_time=5),
    Field(fieldname=FieldName.SHOP_INTRO, css_selector='#hoteldetail'),
    Field(fieldname=FieldName.SHOP_FACILITIES, css_selector='#facility', attr='innerHTML', filter_func=get_shop_facility),
    Field(fieldname=FieldName.SHOP_TRAFFIC, css_selector='#traffic', attr='innerHTML', filter_func=get_shop_traffic),
    Field(fieldname=FieldName.SHOP_STATISTICS, css_selector='#comments', attr='innerHTML', filter_func=get_shop_statistics),
)

page_shop_1 = Page(name='驴妈妈酒店店铺列表页面', fieldlist=fl_shop1, listcssselector=ListCssSelector(list_css_selector='#mainHotelLeft > div'), mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection))

page_shop_2 = Page(name='驴妈妈酒店店铺详情页面', fieldlist=fl_shop2, tabsetup=TabSetup(click_css_selector='dl > dt > a'),mongodb=Mongodb(db=TravelDriver.db, collection=TravelDriver.shop_collection), is_save=True)

class LvmamaHotelSpider(TravelDriver):

    def get_shop_info(self):
        try:
            shop_data_list = self.from_page_get_data_list(page=page_shop_1)
            self.from_page_add_data_to_data_list(page=page_shop_2, data_list=shop_data_list, pre_page=page_shop_1)
        except Exception as e:
            self.error_log(e=e)

    def get_shop_info_list(self):
        self.fast_get_page(url='http://hotels.lvmama.com/hotel/')
        time.sleep(2)
        self.until_send_text_by_css_selector(css_selector='#js_mdd',text=self.data_region)
        time.sleep(1)
        self.until_send_enter_by_css_selector(css_selector='#js_mdd')
        self.until_send_text_by_css_selector(css_selector='#js_keyword',text=self.data_region)
        time.sleep(1)
        self.until_send_enter_by_css_selector(css_selector='#js_keyword')
        time.sleep(1)
        self.fast_click_same_page_by_css_selector(click_css_selector='body > div.banWrap.pr > div.hotelSeach.fix.pa.yh.f14 > div.hotelSeachbtn.fl.pr.tc.f18')
        time.sleep(1)
        self.vertical_scroll_to()#滚动到页面底部
        self.until_click_no_next_page_by_partial_link_text(link_text='下一页', func=self.get_shop_info)

    def run_spider(self):
        try:
            self.get_shop_info_list()
        except Exception:
            self.error_log()