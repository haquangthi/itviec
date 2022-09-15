# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ItviecItem(scrapy.Item):
    # define the fields for your item here like:
    body = scrapy.Field()
    address = scrapy.Field()
    job_title = scrapy.Field()
    url= scrapy.Field()
    province = scrapy.Field()
    company_name = scrapy.Field()
    country = scrapy.Field()
    no_employee = scrapy.Field()
    description_company = scrapy.Field()
    day_work = scrapy.Field()
    job_skill = scrapy.Field()
    job_description = scrapy.Field()
    data_date = scrapy.Field()
    crawl_date = scrapy.Field()
    pass
