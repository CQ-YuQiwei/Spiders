import scrapy
import json
from tencent.items import TencentItem

class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['careers.tencent.com']
    # start_urls = ['http://careers.tencent.com/']
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1605511913758&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=40001&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1605517128087&postId={}&language=zh-cn'
    start_urls = [one_url.format(1)]

    def parse(self, response):
        for page in range(1, 11):
            url = self.one_url.format(page)

            yield scrapy.Request(
                url=url,
                callback=self.parse_one,
            )

    def parse_one(self, response):
        data = json.loads(response.text)
        # print(data)
        for job in data['Data']['Posts']:
            # print(job)
            item = {}
            item['zh_name'] = job['RecruitPostName']
            item['zh_type'] = job['CategoryName']
            post_id = job['PostId']
            detail_url = self.two_url.format(post_id)

            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_two,
                meta={'item': item}
            )

    def parse_two(self, response):
        # item = response.meta['item']
        item = response.meta.get('item')
        # print(item)
        # print(response.text)
        data = json.loads(response.text)
        item['zh_ibility'] = data['Data']['Responsibility']
        item['zh_requier'] = data['Data']['Requirement']
        # print(item)
        yield item

    def Save(self,list):
        pass