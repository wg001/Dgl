# -*- coding: utf-8 -*-
import json
from fnmatch import translate

import os
import scrapy
from scrapy.http import Request

from DgSpider.items import DgspiderItem


def parse_info(response):
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    print("start parse ......")
    get_arr = response.xpath('//ul[@class="bigimg"]/li')
    print(len(get_arr))
    price = []
    img = []
    title = []
    for child in get_arr:
        img0 = child.xpath('./a/img/@data-original').extract_first()
        if img0 == None:
            img0 = child.xpath('./a/img/@src').extract_first()
        img.append(img0)
        price.append(child.xpath('./p[@class="price"]/span[@class="search_now_price"]/text()').extract_first())
        title.append(child.xpath('./p[@name="title"]/a[@name="itemlist-title"]/text()').extract_first())
    result = ""
    print("img的数量：", len(img))
    print("price的数量：", len(price))
    print("title的数量：", len(title))
    for i in range(len(title)):
        item = DgspiderItem()
        item['title'] = title[i].strip()
        item['price'] = price[i]
        item['img'] = img[i]
        temp = json.dumps(dict(item), ensure_ascii=False)
        result = result + temp
    print(result)
    print("------------------------------------------------------------")
    print(type(result))
    print("------------------------------------------------------------")
    rr = open(path+'/data/textabc123.json', 'wb+').write(result.encode(encoding="utf-8"))
    print(rr)
    print("oooooooooooooooooo")


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    url = "http://category.dangdang.com/pg2-cp01.54.06.00.00.00.html"

    def start_requests(self):
        yield Request(self.url, parse_info)

    def parse(self, response):
        pass
