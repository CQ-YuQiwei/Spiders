from selenium import webdriver
import time
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LagouSpider(object):
    def __init__(self):
        self.url = 'https://www.lagou.com/jobs/list_python/p-city_215?&cl=false&fromSearch=true&labelWords=&suginput='
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def run(self):
        self.driver.get(self.url)
        # 取消页面红包弹出框
        self.driver.find_element_by_class_name('body-btn').click()
        while True:
            # 获取页面源代码
            # sourse = self.driver.page_source
            # self.parse_list_page(sourse)

            time.sleep(1)
            next_btn = WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "page_next")]')))

            # 翻页，点击下一页
            # next_btn = self.driver.find_element_by_class_name('page_next').click()
            # next_btn = self.driver.find_element_by_xpath('//span[contains(@class, "page_next")]')
            # 判断当前页面有没有最后一页的class pager_next pager_next_disabled
            if 'pager_next pager_next_disabled' in next_btn.get_attribute('class'):
                break
            #
            else:
                # 模糊定位
                next_btn.click()

    def parse_list_page(self, sourse):
        # print(sourse)

        html = etree.HTML(sourse)
        links = html.xpath('//a[@class="position_link"]/@href')
        for link in links:
            # print(link)
            self.requests_detail_page(link)
            time.sleep(1)

    def requests_detail_page(self, link):
        self.driver.get(link)
        sourse = self.driver.page_source
        self.parse_detail_page(sourse)

    def parse_detail_page(self, sourse):
        html = etree.HTML(sourse)

        data = []
        job = {}

        job_name = html.xpath('//div[@class="job-name"]/h1/text()')[0]
        job_detail = html.xpath('//div[@class="job-detail"]/p/text()')
        print(job_name, job_detail)

        job['job_name'] = job_name


if __name__ == '__main__':
    lg = LagouSpider()
    lg.run()
