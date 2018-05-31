# -*- coding: utf-8 -*-
import scrapy


class RestaurantsSpider(scrapy.Spider):
    name = 'restaurants'
    allowed_domains = ['www.hotpepper.jp']
    start_urls = ['https://www.hotpepper.jp/index.html']

    def parse(self, response):
        # get all areas
        all_areas = response.xpath('//a[contains(@href,"SA")]')
        # for area in all_areas:
        #     yield {"area_code":area.css('a::attr(href)').extract_first(),
        #            "area_name":area.css('a::text').extract_first()}

        # search links
        base_search_url = "https://www.hotpepper.jp/CSP/psh010/doBasic?FWT=ベトナム　料理&SA="
        search_links = [base_search_url +
                        area.css('a::attr(href)').extract_first().replace('/','') for area in all_areas]

        for link in search_links:
            
            pass

