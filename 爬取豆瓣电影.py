import requests
from lxml import etree
import csv

doubanUrl = 'https://movie.douban.com/top250?start={}&filter='


# 第一步获取网页源码
def getSource(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    return response.text


# 第二步定义一个函数，获取电影信息
def getEveryItem(source):
    html_element = etree.HTML(source)
    movieItemList = html_element.xpath('//div[@class="info"]')

    # 定义一个空列表，展示电影信息
    movieList = []

    for eachMovie in movieItemList:

        # 创建一个字典，向列表中存储数据[{电影一},{电影二}……]
        movieDict = {}

        title = eachMovie.xpath('div[@class="hd"]/a/span[@class="title"]/text()')  # 标题
        otherTitle = eachMovie.xpath('div[@class="hd"]/a/span[@class="other"]/text()')  # 副标题
        link = eachMovie.xpath('div[@class="hd"]/a/@href')[0]  # url
        star = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]  # 评分
        quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()')  # 引言（名句）

        if quote:
            quote = quote[0]
        else:
            quote = ''

        # 保存数据
        movieDict['title'] = ''.join(title + otherTitle)
        movieDict['url'] = link
        movieDict['star'] = star
        movieDict['quote'] = quote
        movieList.append(movieDict)

        print(movieList)
    return movieList


# 保存数据
def writeData(movieList):
    with open('douban1.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'star', 'quote', 'url'])

        writer.writeheader()  # 写入表头

        for each in movieList:
            writer.writerow(each)


if __name__ == '__main__':
    movieList = []

    # 一共有10页
    for i in range(10):
        pageLink = doubanUrl.format(i * 25)
        source = getSource(pageLink)
        movieList += getEveryItem(source)

    writeData(movieList)
