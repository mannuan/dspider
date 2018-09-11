from spider.driver.base.field import FieldName
from spider.driver.travel.core.traveldriver import WEBSITE_NAME_LIST,DataSourceName,TravelDriver
from spider.driver.base.mongodb import Mongodb

shops_collection = Mongodb(host=TravelDriver.host, port=TravelDriver.port, db=TravelDriver.db,
                           collection=TravelDriver.shop_collection).get_collection()
comments_collection = Mongodb(host=TravelDriver.host, port=TravelDriver.port, db=TravelDriver.db,
                              collection=TravelDriver.comments_collection).get_collection()


for i in shops_collection.aggregate([{'$match': {FieldName.DATA_WEBSITE: "大众点评",
                                                    FieldName.DATA_REGION: "千岛湖",
                                                    FieldName.DATA_SOURCE: "餐饮",
                                                    FieldName.SHOP_COMMENT_NUM : {"$gt":0}}},
                                                {'$group': {"_id": "$shop_url", "num": {"$first": "$%s"%FieldName.SHOP_COMMENT_NUM}}},
                                     {'$group': {"_id": None, "sum": {"$sum": "$num"}}}]):
    print(i)