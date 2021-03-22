import scrapy
from yangguang.items import YangguangItem
import re


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&type=4&page=0']
    # 处理列表页
    def parse(self, response):
        li_list = response.xpath('//div[@class="width-12"]/ul[@class="title-state-ul"]/li')

        for li in li_list:
            item = YangguangItem()
            item['title'] = li.xpath('./span[@class="state3"]/a/text()').extract_first()
            item['href'] = 'http://wz.sun0769.com' + li.xpath('./span[@class="state3"]/a/@href').extract_first()

            yield scrapy.Request(
                url=item['href'],
                callback=self.parse_detail,
                meta={'item': item}
            )

        next_url = 'http://wz.sun0769.com' + response.xpath(
            '//div[@class="mr-three paging-box"]/a[2]/@href').extract_first()
        # print(next_url)
        if next_url is not None:
            yield scrapy.Request(
                url=next_url,
                callback=self.parse
            )
    # 处理详情页
    def parse_detail(self, response):
        item = response.meta.get('item')
        item['content'] = response.xpath('//div[@class="details-box"]/pre/text()').extract_first()
        item['content_img'] = response.xpath('//div[@class="clear details-img"]/img/@src').extract_first()
        # print(item)
        yield item
