import scrapy
class SellItem(scrapy.Item):
    code = scrapy.Field()
    release_time = scrapy.Field()
    price_all = scrapy.Field()
    price_per = scrapy.Field()
    first_pay = scrapy.Field()#
    month_pay = scrapy.Field()#
    floor = scrapy.Field()
    area_build = scrapy.Field()
    direction = scrapy.Field()
    decoration = scrapy.Field()#
    house_model = scrapy.Field()
    build_time = scrapy.Field()
    house_structure = scrapy.Field()
    house_type = scrapy.Field()
    property_type = scrapy.Field()