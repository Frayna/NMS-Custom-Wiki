# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NmsRessourceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    type = scrapy.Field()
    rarity = scrapy.Field()
    value = scrapy.Field()
    usedFor = scrapy.Field()
    symbol = scrapy.Field()
    img = scrapy.Field()
