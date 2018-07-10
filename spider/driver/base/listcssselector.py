# -*- coding:utf-8 -*-

class ListCssSelector(object):
    def __init__(self, list_css_selector='', item_css_selector='', item_start=0, item_end=0):
        """

        :param list_css_selector:
        :param item_css_selector:
        :param item_start:默认为0表示未设置,从1开始计数
        :param item_end:默认为0表示未设置,位置可以和item_start重叠
        eg. 选取第五个和第六个可以是:item_start=5,item_end=6
        """
        self.list_css_selector = list_css_selector
        self.item_css_selector = item_css_selector
        self.item_start = item_start
        self.item_end = item_end

    def __str__(self):
        if not self.list_css_selector:
            return str(None)
        else:
            result = vars(self).copy()
            if not self.item_end:
                result.pop('item_end')
            if not self.item_css_selector:
                result.pop('item_css_selector')
            return str(result)

    def __eq__(self, other):
        if other is None:
            return not self.list_css_selector
        else:
            if vars(other) == vars(self):
                return True
            else:
                super.__eq__(self, other)