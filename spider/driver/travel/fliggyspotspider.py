# -*- coding:utf-8 -*-

from spider.driver.travel.core.traveldriver import *
from .params import *
from .fields import *

class FliggySpotSpider(TravelDriver):
    def get_comment_info2(self,shop_data):
        params_list_comment1 = self.params_dict.get(ParamType.COMMENT_INFO_1)  # 获取爬虫数据列表的样式信息
        comment_len = shop_data.get(FieldName.SHOP_COMMENT_NUM)
        self.ismore_by_scroll_page_judge_by_len(css_selector=params_list_comment1.list_css_selector,comment_len=comment_len)
        try:
            for each in self.until_presence_of_all_elements_located_by_css_selector(
                    css_selector=params_list_comment1.list_css_selector+'>div.rate-content-container > div.button-open'):
                self.until_click_by_vertical_scroll_page_down(click_ele=each)
        except Exception as e:
            self.error_log(e=e)
        #上面在下拉加载页面
        external_key={
            FieldName.SHOP_URL : shop_data.get(FieldName.SHOP_URL),
            FieldName.SHOP_NAME : shop_data.get(FieldName.SHOP_NAME),
        }
        self.get_spider_data_list(params_list=params_list_comment1,is_save=True,external_key=external_key,target=self.comments_collections)

    def get_comment_info(self):
        for shop_data in self.get_current_data_list_from_db(self.shops_collections):
            url = shop_data.get(FieldName.COMMENT_URL)
            if url:
                self.run_new_tab_task(func=self.get_comment_info2,url=url,shop_data=shop_data)

    def get_shop_info(self):
        self.logger.info('进入%s移动版主页' % (self.data_website))
        self.driver.get('https://h5.m.taobao.com/trip/home/index.html')
        self.until_click_by_css_selector(
            css_selector='#J_Page > article > header > div > div.searchbar__search___3oyby > p > span')
        self.until_send_text_by_css_selector(
            css_selector='#app > div > div > div.searchsuggestion-container > div.searchinput-theme-yellow.searchinput-container > form > div > div > input',
            text=self.data_region)
        self.info_log(data='输入%s...' % (self.data_region))
        self.until_send_enter_by_css_selector(
            css_selector='#app > div > div > div.searchsuggestion-container > div.searchinput-theme-yellow.searchinput-container > form > div > div > input')
        self.info_log(data='搜索%s' % (self.data_region))
        self.until_click_by_css_selector(
            css_selector='#app > div > div.search-result-ctn > div > div > div > div:nth-child(2) > div > div.h-bar-tabview > div > div.h-tabview-list > div > div > div > ul > li:nth-child(6)')
        self.info_log(data='点击门票...')

        params_list_shop1 = self.params_dict.get(ParamType.SHOP_INFO_1)#获取爬虫数据列表的样式信息

        self.until_ismore_by_send_key_arrow_down_judge_by_len(
            list_css_selector=params_list_shop1.list_css_selector,
            ele_css_selector='#app > div > div.search-result-ctn > div > div > div > div:nth-child(2) > div > div.h-bar-tabview > div > div.h-tabview-list > div > div > div > ul > li.h-tabview-navtab.h-tabview-selected')

        shop_data_list = self.get_spider_data_list(params_list=params_list_shop1)
        params_shop2 = self.params_dict.get(ParamType.SHOP_INFO_2)
        shop_data_list = self.add_spider_data_to_data_list(data_list=shop_data_list,isnewtab=True,params=params_shop2,url_name=FieldName.SHOP_URL)
        params_shop3 = self.params_dict.get(ParamType.SHOP_INFO_3)
        shop_data_list = self.add_spider_data_to_data_list(data_list=shop_data_list, isnewtab=True, params=params_shop3,url_name=FieldName.SHOP_DETAIL_URL)
        for shop_data in shop_data_list:
            key = {
                FieldName.SHOP_URL: shop_data.get(FieldName.SHOP_URL),
                FieldName.SHOP_NAME : shop_data.get(FieldName.SHOP_NAME),
            }
            self.save_data_to_db(target=self.shops_collections,key=key,data=shop_data)

    def run_spider(self):
        self.get_shop_info()
        self.get_comment_info()