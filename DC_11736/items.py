# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Dc11736Item(scrapy.Item):
    url = scrapy.Field()
    document_id = scrapy.Field()
    fulltext = scrapy.Field()
    fulltext_content_type = scrapy.Field()
    title = scrapy.Field()
    publication_date = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    seed_url = scrapy.Field()
    labels = scrapy.Field()
    abstract = scrapy.Field()
    topic_id = scrapy.Field()
    tag = scrapy.Field()
    product_category_id = scrapy.Field()

    raw_content = scrapy.Field()
    raw_content_type = scrapy.Field()
