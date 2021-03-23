# https://www.doutula.com/photo/list/?page=1 第一页

# https://www.doutula.com/photo/list/?page=2 第二页

# https://www.doutula.com/photo/list/?page=3 第三页

import requests

from lxml import etree

import os

from time import *

from queue import Queue

import threading

start = time()


# 定义生产者对象
class Procuder(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }

    def __init__(self, page_queue, img_queue, *args, **kwargs):

        super(Procuder, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):

        while True:
            # 如果队列没有数据就退出循环
            if self.page_queue.empty():
                break

            # 拿到网页的url
            url = self.page_queue.get()

            # 调用解析网页的函数
            self.parse_page(url)

    # 定义一个函数来解析网页
    def parse_page(self, url):

        response = requests.get(url, headers=self.headers)

        # print(response.text)
        # 网页源码
        text = response.text

        html = etree.HTML(text)
        # 获取Img 并且把gif的图片过滤掉
        imgs = html.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')

        for img in imgs:
            # print(etree.tostring(img))
            # 获取每张图片的url
            img_url = img.get('data-original')

            # 获取图片的名字
            alt = img.get('alt')

            # 在os模块中可以很好的分割字符，比如这种带.的数据
            suffix = os.path.splitext(img_url)[1]

            # 把图片的名字进行拼接
            filename = alt + suffix
            # print(filename)

            # 保存图片
            with open('img/' + filename, 'wb') as f:
                img_rep = requests.get(img_url)

                f.write(img_rep.content)


# 定义消费者对象
class Consumer(threading.Thread):

    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):

        while True:

            if self.img_queue.empty() and self.page_queue.empty():
                break

            img_url, filename = self.img_queue.get()

            # 保存图片
            with open('img/' + filename, 'wb') as f:
                img_rep = requests.get(img_url)

                f.write(img_rep.content)


def main():
    # 定义页数的队列
    page_queue = Queue(100)

    # 定义图片的url
    img_queue = Queue(500)

    for x in range(1, 2):

        # print(x)
        url = 'https://www.doutula.com/photo/list/?page=%d' % x
        # parse_page(url)

        # 把页数添加到队列中
        page_queue.put(url)

        # 创建生产者和消费者
        # 创建生产者
        for x in range(5):
            t = Procuder(page_queue, img_queue)
            t.start()

        # 创建消费者
        for x in range(5):
            t = Consumer(page_queue, img_queue)
            t.start()


if __name__ == '__main__':
    main()
    end = time()
    print('程序共花费了:', end - start)
