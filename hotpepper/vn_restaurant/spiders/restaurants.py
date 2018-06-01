# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class RestaurantsSpider(scrapy.Spider):
    name = 'restaurants'
    allowed_domains = ['www.hotpepper.jp']
    start_urls = ['https://www.hotpepper.jp']
    count_parse = 0
    count_search_page = 0
    count_page = 0

    def parse(self, response):
        # get all areas
        all_areas = response.xpath('//ul[@class="areaSelectList"]/li/dl/dd/a')
        # for area in all_areas:
        #     print( {"area_code":area.css('a::attr(href)').extract_first(),
        #            "area_name":area.css('a::text').extract_first()})

        # search links
        base_search_url = "https://www.hotpepper.jp/CSP/psh010/doBasic?FWT=ベトナム%20料理&SA="
        search_links = [base_search_url +
                        area.css('a::attr(href)').extract_first().replace('/','') for area in all_areas]


        for link in search_links:
            yield Request(link, callback=self.parse_search_page)

    def parse_search_page(self, response):
        shops_detail = response.xpath('//h3[contains(@class,"shopDetailStoreName")]/a')
        shops_detail_links = [self.start_urls[0] + shop_detail.css('a::attr(href)').extract_first() for shop_detail in shops_detail]
        # yield ({"link": response.url})

        for shop_detail_link in shops_detail_links:
            # yield ({"link":shop_detail_link})
            yield Request(shop_detail_link, callback=self.parse_shop_detail_page)

        # process next page
        next_page_ul = response.xpath('//ul[@class="searchResultPageLink cf"]/li/a')

        for next_page in next_page_ul:
            if next_page.extract().find("次") > -1:
                next_page_url = next_page.css('a::attr(href)').extract_first()
                absolute_next_page_url = self.start_urls[0] + next_page_url
                yield Request(absolute_next_page_url, callback=self.parse_search_page)

    def parse_shop_detail_page(self, response):
        shop_name = response.xpath('//h1[@class="shopName"]/text()').extract_first()
        shop_adr = response.xpath('//table[@class="infoTable"]/tbody/tr/td/address/text()').extract_first()
        shop_info = response.xpath('//table[@class="infoTable"]/tbody/tr')

        shop_adr = ''
        for info in shop_info:
            if info.xpath('.//th/text()').extract_first().find("住所") > -1:
                if info.xpath('.//td/address/text()').extract_first():
                    shop_adr = info.xpath('.//td/address/text()').extract_first()
                else:
                    shop_adr = info.xpath('.//td/text()').extract_first()

        if shop_adr != '':
            yield {"shop_name":shop_name, "shop_adr":shop_adr.replace("\n","")}
        else:
            print("shop adr is null")









