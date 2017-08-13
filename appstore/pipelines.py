# -*- coding: utf-8 -*-
import pymongo

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


######## the pipeline not for MONGODB
class AppstorePipeline(object):
	def __init__(self):
		self.file = open('appstore.dat', 'wb')

	def process_item(self, item, spider):
		val = "{0}\t{1}\t{2}\t{3}\t{4}\n".format(item['appid'], item['title'], item['intro'], item['thumbnail'], item['recommened'])
		self.file.write(val)
		return item

######## the pipeline for MONGODB
# class AppstoreMongodbPipeline(object):
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db

#     @classmethod
#     def from_crawler(cls, crawler):
#         """
#         return an instance of this pipeline
#         crawler.settings --> settings.py
#         get mongo_uri & mongo_database from settings.py
#         :param crawler:
#         :return: crawler instance
#         """
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE')
#         )

#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]

#     def close_spider(self, spider):
#         self.client.close()

#     def process_item(self, item, spider):
#         """
#         process data here before loading to mongodb
#         :param item:
#         :param spider:
#         :return: item
#         """
#         collection_name = item.__class__.__name__  # use itemName as the collectionName
#         # self.db[collection_name].remove({}) # clean the collection when new crawling starts
#         self.db[collection_name].insert(dict(item))
#         # return item