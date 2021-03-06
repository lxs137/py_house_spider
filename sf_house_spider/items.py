import scrapy
class URLItem(scrapy.Item):
    region = scrapy.Field()
    url = scrapy.Field()

class CommunityItem(scrapy.Item):
    name = scrapy.Field()
    region = scrapy.Field()
    page_url = scrapy.Field()
    sell_url = scrapy.Field()
    rent_url = scrapy.Field()
    record_url = scrapy.Field()
    price_cur = scrapy.Field()
    ratio_month = scrapy.Field()
    address = scrapy.Field()
    community_feature = scrapy.Field()
    property = scrapy.Field()
    manage_type = scrapy.Field()
    done_time = scrapy.Field()
    build_company = scrapy.Field()
    building_type = scrapy.Field()
    building_area = scrapy.Field()
    cover_area = scrapy.Field()
    house_num_cur = scrapy.Field()
    house_num_sum = scrapy.Field()
    green_rate = scrapy.Field()
    volum_rate = scrapy.Field()
    manage_price = scrapy.Field()
    info_add = scrapy.Field()
    water_price = scrapy.Field()
    electric_price = scrapy.Field()
    gas_price = scrapy.Field()
    network = scrapy.Field()
    elector = scrapy.Field()
    security = scrapy.Field()
    sanitation = scrapy.Field()
    parking = scrapy.Field()
    metro = scrapy.Field()
    bus = scrapy.Field()
    car = scrapy.Field()
    kindergarten = scrapy.Field()
    school = scrapy.Field()
    university = scrapy.Field()
    shop_mall = scrapy.Field()
    hospital = scrapy.Field()
    post_office = scrapy.Field()
    bank = scrapy.Field()
    other_facility = scrapy.Field()