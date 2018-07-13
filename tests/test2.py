#使用pickle模块将数据对象保存到文件

from spider.driver.base.mongodb import Mongodb

shop_collection = Mongodb(db='dspider2',collection='shops', host='10.1.17.15').get_collection()
count = 0
for i in shop_collection.find({'data_website':'大众点评','data_region':'千岛湖','data_source':'餐饮'}):
    if len(i.keys()) < 21:
        count += 1
    elif len(i.get('shop_address').replace(' ','')) < 8 and i.get('shop_address'):
        count += 1
        print(i.get('shop_address'))
print(count)