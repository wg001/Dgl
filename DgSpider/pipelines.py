# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os


class DgspiderPipeline(object):
    path = os.path.abspath(os.path.dirname(__file__))
    file = None

    def __init__(self):
        if self.file is None:
            self.file = open(self.path + "/data/data.txt", 'a+', encoding='utf-8')
        pass

    def process_item(self, item, spider):
        strval = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(strval + "\n")
        print(item)
        return item
