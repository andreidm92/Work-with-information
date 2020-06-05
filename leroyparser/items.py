# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.loader.processors import MapCompose, TakeFirst
import scrapy

def cleaner_photo(value):
    if value[:2] == '//':
        return f'http:{value}'
    return value

def price_int(value):
    return int(value.replace(" ", ""))

def work_str(v_str):
    v_str = ''.join(v_str).split()
    return v_str


class LeroyparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_int))
    product_link = scrapy.Field()
    photo = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    n_char = scrapy.Field()
    v_char = scrapy.Field(input_processor=work_str)





