# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class YangguangPipeline:
    def process_item(self, item, spider):
        # item['content'] = self.parse_content(item['content'])
        # if len(item['content_img']) == 0:
        #     item['content_img'] = '该贴暂无图片'
        print(item)
        return item

    # def parse_content(self,content):
    #     content = [re.sub(r'\xa0|\r\n\t','', i) for i in content]
    #       content = [i for i in content if len(i)>0]
    #     return content
