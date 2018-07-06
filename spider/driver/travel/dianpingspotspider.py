# -*- coding:utf-8 -*-

from spider.driver.travel.core.traveldriver import *
from .params import *
from .fields import *

class DianpingSpotSpider(TravelDriver):
    def getCommentInfo2(self,shop_id,shop_name,comment_list_url,page):
        self.logger.info('commentinfo2')
        item_count = 0
        # 点击展开评论
        for each in self.driver.find_elements_by_css_selector(
                '#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li > div > div.review-truncated-words > div > a'):
            self.logger.info('正在展开评论...')
            each.click()

        for each in self.driver.find_elements_by_css_selector(
                '#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li'):
            item_count += 1
            # ActionChains(driver).move_to_element(each).perform()
            try:
                comment_user_name = each.find_element_by_css_selector('div > div.dper-info > a').text
            except Exception as e:
                self.ErrorLog(field='comment_user_name',e=e)
                continue
            self.InfoLog(field='comment_user_name',data=comment_user_name)
            try:
                comment_user_url = each.find_element_by_css_selector('div > div.dper-info > a').get_attribute('href')
            except Exception as e:
                self.ErrorLog(field='comment_user_url', e=e)
            try:
                comment_user_pic = each.find_element_by_css_selector('a > img').get_attribute('src')
            except Exception as e:
                self.ErrorLog(field='comment_user_pic', e=e)
                comment_user_pic = ''
            try:
                comment_time = each.find_element_by_css_selector('div > div.misc-info.clearfix > span.time').text
            except Exception as e:
                self.ErrorLog(field='comment_time', e=e)
                comment_time = ''
            self.InfoLog(field='comment_time', data=comment_time)
            try:
                comment_star = each.find_element_by_css_selector('div > div.review-rank > span').get_attribute('class')
                comment_star = float(re.sub(r'[^\d]*', r'', comment_star)) / 10
            except Exception as e:
                self.ErrorLog(field='comment_star', e=e)
                comment_star = 0
            try:
                comment_content = each.find_element_by_css_selector('div > div.review-words').text
                comment_content = re.sub(r'[\n]*', r'', comment_content).replace('收起评论', '')
            except Exception as e:
                self.ErrorLog(field='comment_content', e=e)
            comment_img = list()
            try:
                review_pic = each.find_element_by_css_selector('div > div.review-pictures')
                for each1 in review_pic.find_elements_by_css_selector('ul > li'):
                    comment_img.append(each1.find_element_by_css_selector('a > img').get_attribute('data-lazyload'))
            except Exception as e:
                self.ErrorLog(field='comment_img', e=e)
            comment_like_replay = each.find_element_by_css_selector('div.content > div.misc-info > span.actions').text
            try:
                comment_like = int(re.sub(r'[^\d]*', r'', comment_like_replay.split('回应')[0]))
            except Exception as e:
                self.ErrorLog(field='comment_like', e=e)
                comment_like = 0
            try:
                comment_replay = int(re.sub(r'[^\d]*', r'', comment_like_replay.split('回应')[1]))
            except Exception as e:
                self.ErrorLog(field='comment_replay', e=e)
                comment_replay = 0
            comment_data = {
                'shop_id': shop_id,
                'shop_name': shop_name,
                'comment_list_url': comment_list_url,
                'comment_user_name': comment_user_name,
                'comment_user_url': comment_user_url,
                'comment_user_pic': comment_user_pic,
                'comment_time': comment_time,
                'comment_star': comment_star,
                'comment_content': comment_content,
                'comment_img': comment_img,
                'comment_like': comment_like,
                'comment_replay': comment_replay,
                'page': page,
                'item_count': item_count,
            }
            key = {
                'shop_id': shop_id,
                'shop_name': shop_name,
                'comment_user_name': comment_user_name,
                'comment_time': comment_time,
            }
            self.SaveData(target=self.comments, key=key, data=comment_data)


    def get_comment_info2(self,shop_data):
        page = 1
        while (True):  # 加载全部评论
            self.info_log(data='正在浏览第%s'%page)
            # 点击展开评论
            try:
                for each in self.until_presence_of_all_elements_located_by_css_selector(css_selector='#review-list > div.review-list-container > div.review-list-main > div.reviews-wrapper > div.reviews-items > ul > li > div > div.review-truncated-words > div > a'):
                    self.logger.info('正在展开评论...')
                    self.until_click_by_vertical_scroll_page_down(click_ele=each)
            except Exception as e:
                self.error_log(e=e)

            params_list_comment1 = self.params_dict.get(ParamType.COMMENT_INFO_1)
            external_key = {
                FieldName.SHOP_URL: shop_data.get(FieldName.SHOP_URL),
                FieldName.SHOP_ID: shop_data.get(FieldName.SHOP_ID),
                FieldName.SHOP_NAME: shop_data.get(FieldName.SHOP_NAME),
            }
            self.get_spider_data_list(params_list=params_list_comment1, is_save=True, external_key=external_key,
                                      target=self.comments_collections)
            try:
                self.until_click_by_partial_link_text(link_text='下一页').click()
                page +=1
                # 产生随机暂停时间
                pause_time = self.get_random_time(a=9999,b=99999,d=777)
                self.info_log(data='...随机暂停:{}s...'.format(pause_time))
                time.sleep(pause_time)
            except Exception as e:
                # pause_time = self.get_random_time(a=9999, b=99999, d=222)
                # self.info_log(data='...随机暂停:{}s...'.format(pause_time))
                # time.sleep(pause_time)
                break

    def get_comment_info(self):
        for shop_data in self.get_current_data_list_from_db(self.shops_collections):
            url = shop_data.get(FieldName.SHOP_URL)+'/review_all'
            if url:
                self.run_new_tab_task(func=self.get_comment_info2,url=url,shop_data=shop_data)

    def get_shop_info(self):
        self.info_log(data='进入%s移动版主页...'%(self.data_website))
        self.driver.get('https://m.dianping.com/')
        time.sleep(2)
        self.until_click_by_css_selector(css_selector='body > div.J_header > header > div.search.J_search_trigger')
        self.info_log(data='输入%s...'%(self.data_region))
        self.until_send_text_by_css_selector(
            css_selector='body > div.J_search_container.search_container > form > div.head_cnt > div > input.J_search_input',
            text=self.data_region)
        self.info_log(data='搜索%s...'%(self.data_region))
        self.until_send_enter_by_css_selector(
            css_selector='body > div.J_search_container.search_container > form > div.head_cnt > div > input.J_search_input')
        self.info_log(data='选择周边游...')
        self.until_click_by_link_text(link_text='全部分类')
        scrollbar = self.until_presence_of_element_located_by_css_selector(
            css_selector='#app > div > div.J_searchList > nav > section:nth-child(3) > div.menu.main > div.iScrollVerticalScrollbar.iScrollLoneScrollbar > div')
        ActionChains(self.driver).click_and_hold(scrollbar).move_by_offset(0, -100).click(scrollbar).perform()
        self.until_click_by_css_selector(css_selector='#app > div > div.J_searchList > nav > section:nth-child(3) > div.menu.main > div:nth-child(1) > div:nth-child(8)')
        self.until_click_by_link_text(link_text=self.data_source)
        self.info_log(data='选择%s...'%(self.data_source))
        while (True):
            self.vertical_scroll_by(offset=1000)
            try:
                self.until_presence_of_element_located_by_css_selector(css_selector='#app > div > div.J_footer')
                break
            except Exception as e:
                self.error_log(name='下拉页面', e=e)

        params_list_shop1 = self.params_dict.get(ParamType.SHOP_INFO_1)
        shop_data_list = self.get_spider_data_list(params_list=params_list_shop1)
        for i in range(len(shop_data_list)):
            url = shop_data_list[i][FieldName.SHOP_URL].replace('m.dianping.com','www.dianping.com')
            shop_data_list[i][FieldName.SHOP_URL] = url
        params_shop2 = self.params_dict.get(ParamType.SHOP_INFO_2)
        shop_data_list = self.add_spider_data_to_data_list(data_list=shop_data_list, isnewtab=True, params=params_shop2,
                                                           url_name=FieldName.SHOP_URL)
        for shop_data in shop_data_list:
            key = {
                FieldName.SHOP_URL: shop_data.get(FieldName.SHOP_URL),
                FieldName.SHOP_ID: shop_data.get(FieldName.SHOP_ID),
                FieldName.SHOP_NAME : shop_data.get(FieldName.SHOP_NAME),
            }
            self.save_data_to_db(target=self.shops_collections,key=key,data=shop_data)

    def run_spider(self):
        # self.get_shop_info()
        self.get_comment_info()
