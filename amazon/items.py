# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    product_name = scrapy.Field()
    price = scrapy.Field()
    quantity = scrapy.Field()
    stock_status = scrapy.Field()
    delivery_date = scrapy.Field()
    days_delivered = scrapy.Field()
    # pass
