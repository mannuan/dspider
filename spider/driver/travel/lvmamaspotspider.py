# -*- coding:utf-8 -*-

from spider.driver.travel.core.traveldriver import *
from .params import *
from .fields import *

class LvmamaSpotSpider(TravelDriver):
    def get_comment_info2(self,shop_data):
        params_list_comment1 = self.params_dict.get(ParamType.COMMENT_INFO_1)  # 获取爬虫数据列表的样式信息
        comment_len = shop_data.get(FieldName.SHOP_COMMENT_NUM)
        while(True):
            comments_list_len = self.until_presence_of_all_elements_located_by_css_selector(
                css_selector=params_list_comment1.list_css_selector)
            if comments_list_len < comment_len*0.7:
                self.driver.refresh()
                time.sleep(0.5)
            else:
                break
        self.ismore_by_scroll_page_judge_by_len(css_selector=params_list_comment1.list_css_selector,comment_len=comment_len)
        try:
            for each in self.until_presence_of_all_elements_located_by_css_selector(
                    css_selector=params_list_comment1.list_css_selector+' > div.arrow'):
                self.until_click_by_vertical_scroll_page_down(click_ele=each)
        except Exception as e:
            self.error_log(e=e)
        #上面在下拉加载页面
        external_key={
            FieldName.SHOP_URL : shop_data.get(FieldName.SHOP_URL),
            FieldName.SHOP_ID : shop_data.get(FieldName.SHOP_ID),
            FieldName.SHOP_NAME : shop_data.get(FieldName.SHOP_NAME),
        }
        self.get_spider_data_list(params_list=params_list_comment1,is_save=True,external_key=external_key,target=self.comments_collections)

    def get_comment_info(self):
        for shop_data in self.get_current_data_list_from_db(self.shops_collections):
            url = shop_data.get(FieldName.COMMENT_URL)
            if url:
                self.run_new_tab_task(func=self.get_comment_info2,url=url,shop_data=shop_data)

    def get_shop_info(self):
        self.info_log(data='进入驴妈妈移动版主页...')
        self.driver.get('https://m.lvmama.com')
        time.sleep(1.5)
        self.until_click_by_css_selector(css_selector='#content > div.index-header > a.search.cmAddClick > p')
        time.sleep(1)
        self.until_send_text_by_css_selector(css_selector='#keyword',text=self.data_region)
        self.info_log(data='输入%s...'%self.data_region)
        self.until_send_enter_by_css_selector(css_selector='#keyword')
        self.info_log(data='搜索%s...'%self.data_region)
        time.sleep(1)
        self.until_click_by_css_selector(css_selector='#tab_ticket > a')
        self.info_log(data='点击%s门票...'%self.data_source)
        time.sleep(3)
        for i in range(200):
            ActionChains(self.driver).move_to_element(
                self.driver.find_element_by_css_selector(
                    'body > div.headBlank > div.headFixed > div > nav > div')).send_keys(Keys.ARROW_DOWN).perform()

        self.info_log(data='shopinfo')
        params_list_shop1 = self.params_dict.get(ParamType.SHOP_INFO_1)  # 获取爬虫数据列表的样式信息
        shop_data_list = self.get_spider_data_list(params_list=params_list_shop1,end=18)
        params_shop2 = self.params_dict.get(ParamType.SHOP_INFO_2)
        shop_data_list = self.add_spider_data_to_data_list(data_list=shop_data_list, isnewtab=True, params=params_shop2,
                                                           url_name=FieldName.SHOP_URL)
        for shop_data in shop_data_list:
            key = {
                FieldName.SHOP_URL: shop_data.get(FieldName.SHOP_URL),
                FieldName.SHOP_ID: shop_data.get(FieldName.SHOP_ID),
                FieldName.SHOP_NAME : shop_data.get(FieldName.SHOP_NAME),
            }
            self.save_data_to_db(target=self.shops,key=key,data=shop_data)

    def run_spider(self):
        self.get_shop_info()
        self.get_comment_info()
