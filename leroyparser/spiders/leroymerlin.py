# -*- coding: utf-8 -*-
import scrapy
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, product):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={product}&family=linoleum-201709&suggest=true']

    def parse(self, response):
        next_page = response.xpath("//a[@class='paginator-button next-paginator-button']/@href").extract_first()
        ads_links = response.xpath("//div[@class ='product-name']/a/@href").extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)
        yield response.follow(next_page, callback=self.parse)
    def parse_ads(self, response):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("price", "//span[@slot='price']/text()")
        loader.add_value("product_link", response.url)
        loader.add_xpath("photo", "//picture[@slot='pictures']/img/@src")
        loader.add_xpath("n_char", "//dt[@class='def-list__term']/text()")
        loader.add_xpath("v_char", "//dd[@class='def-list__definition']/text()")
        yield loader.load_item()







