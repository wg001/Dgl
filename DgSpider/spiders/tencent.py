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
    file_id = 5
    for i in range(len(title)):
        item = DgspiderItem()
        item['title'] = title[i].strip()
        item['price'] = price[i]
        item['img'] = img[i]
        # temp = json.dumps(dict(item), ensure_ascii=False)
        yield item
    # print(result)
    # print("------------------------------------------------------------")
    # print(type(result))
    # print("------------------------------------------------------------")
    # rr = open(path+'/data/textabc123.json', 'wb+').write(result.encode(encoding="utf-8"))
    # print(rr)
    # print("oooooooooooooooooo")


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    # url = "http://category.dangdang.com/pg2-cp01.54.06.00.00.00.html"
    url = "http://www.sdgzxh.org/NewsList.aspx?CategoryTitle=%u901a%u77e5%u516c%u544a"
    domain = "http://www.sdgzxh.org/"
    ip_proxy = "http://ip.filefab.com/index.php"
    ip_proxy1 = "http://118.24.27.16/"
    page_s = 1
    page_total = None

    def start_requests(self):
        try:
            yield Request(self.ip_proxy1, self.test_proxy)
        except:
            print("ffffffffffffffffffff")
        # yield from self.testfun()

    def parse(self, response):
        pass

    def testfun(self):
        print("askdfskdfasdf")
        pass

    def test_proxy(self, response):
        print("---------------------------------")
        print(response.text)
        pass

    def parse_other(self, response):
        get_arr = response.xpath('//tr[@class="word3"]')
        total_page = response.xpath('//span[@id="dataGridPageControl1_lblPage"]/text()').extract_first()
        input = response.xpath('//form[@id="form1"]')

        postdata = dict()
        for inp in input:
            name = inp.xpath('./input[@type="hidden"]/@name').extract()
            value = inp.xpath('./input[@type="hidden"]/@value').extract()
            for k in range(len(name)):
                postdata[name[k]] = value[k]
        print(postdata)
        self.logger.info("获取到的总页数：")
        print(total_page[1])
        for child in get_arr:
            item = DgspiderItem()
            src = child.xpath('./td')
            res = src[2].xpath('./a/@href').extract_first()
            text = child.xpath('./td/a/text()').extract_first()
            if res is "#":
                item['address'] = res
            else:
                item['address'] = self.domain + res
            item['text'] = text
            yield item
        yield scrapy.FormRequest(
            url=self.url,
            formdata=postdata,
            callback=self.parse_other
        )
