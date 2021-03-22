import scrapy


class SnSpider(scrapy.Spider):
    name = 'sn'
    allowed_domains = ['suning.com']
    start_urls = ['http://book.suning.com/']

    def parse(self, response):
        # 首页大分类
        li_list = response.xpath('//div[@class="menu-list"]//dl')
        for li in li_list:
            print(li)
            item = {}
            item['b_cate'] = li.xpath('./dt/h3/a/text()').extract_first()
            dd_list = li.xpath('./dd/a')
            for dd in dd_list:
                item['s_href'] = dd.xpath('./@href').extract_first()
                item['s_cate'] = dd.xpath('./text()').extract_first()
                # print(item)
                yield scrapy.Request(
                    url=item['s_href'],
                    callback=self.parse_book_list,
                    meta={'item': item}
                )

    def parse_book_list(self,response):
        item = response.meta.get('item')
        # print(item)
        li_list = response.xpath('//ul[@class="clearfix"]/li')
        for li in li_list:
            item['book_name'] = li.xpath('//div[@class="res-img"]//a/img/@alt').extract_first()
            item['book_image'] = li.xpath('//div[@class="res-img"]//a/img/@src').extract_first()
            item['href'] = li.xpath('//div[@class="res-img"]//a/@href').extract_first()
            if item['href'] is not None:
                item['href'] = 'http:' + item['href']
            # print(item)

                yield scrapy.Request(
                    url=item['href'],
                    callback=self.parse_book_detail,
                    meta={'item': item}
                )
    def parse_book_detail(self,response):
        item = response.meta.get('item')
        # print(item)
        ul = response.xpath('//ul[@class="bk-publish clearfix"]/li')
        for li in ul:
            item['book_author'] = li.xpath('./text()').extract_first()
            # print(item)

