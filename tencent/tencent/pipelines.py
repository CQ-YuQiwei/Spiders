# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from tencent.items import TencentItem


class TencentPipeline:
    def process_item(self, item, spider):
        print(item)
        if isinstance(item, TencentItem):
            print('当前item来自TencentItem')
        return item
