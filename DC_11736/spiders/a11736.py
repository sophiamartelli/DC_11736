import re

import scrapy
from bs4 import BeautifulSoup as bs

from DC_11736.items import Dc11736Item
from DC_11736.settings import SEEDS

DOCUMENT_ID_RGX = r"^https?://(?:www\.)?.*?\.com/(.+)"
DOCUMENT_ID_PREFIX = "FSSAI"

DOCUMENTS_XP = "//article[contains(@class,'fusion-post-medium')]"
TITLE = ".//div[@class='fusion-post-content post-content']//h2/a/text()"
URL = ".//div[contains(@class, 'fusion-alignright')]/a/@href"
ABSTRACT = ".//div[@class='fusion-post-content post-content']/div[@class='fusion-post-content-container']/p/text()"
TAG = ".//div[@class='fusion-meta-info']/div[@class='fusion-alignleft']/a/text()"
AUTHOR = 'FSSAI'

NEXT_PAGE = "//div[@id='posts-container']/div[@class='pagination clearfix']/a[@class='pagination-next']/@href"
TEXT = "//div[contains(@class, 'post-content')]"
FULLTEXT_CONTENT_TYPE = "text/html; charset=utf-8"


class A11736Spider(scrapy.Spider):
    name = 'DC_11736'
    allowed_domains = ['www.fssaifoodlicense.com']
    start_urls = SEEDS

    def parse(self, response):
        if "/blog" in response.url:
            documents = response.xpath(DOCUMENTS_XP)
            for doc in documents:
                url = doc.xpath(URL).extract_first()
                item = Dc11736Item()
                item["title"] = doc.xpath(TITLE).get()
                item["abstract"] = doc.xpath(ABSTRACT).get()
                item["tag"] = doc.xpath(TAG).get()
                item["seed_url"] = response.url

                yield scrapy.Request(url=url, callback=self.parse_html, meta={"item": item})

            else:
                next_page = response.xpath(NEXT_PAGE).get()
                if next_page:
                    yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_html(self, response):
        item = response.meta.get("item")
        item["fulltext"] = generate_fulltext(response.xpath(TEXT).getall())
        item["fulltext_content_type"] = FULLTEXT_CONTENT_TYPE
        item["document_id"] = generate_document_id(response.url)
        item["url"] = response.url
        item["author"] = AUTHOR

        yield item


def prettify_text(text):
    text = " ".join(text)
    return re.sub(r"\s+", " ", text).strip().replace("\r", "").replace("\n", "").replace("\t", "").strip()


def generate_fulltext(fulltext):
    fulltext = " ".join(fulltext)
    fulltext = bs(fulltext).prettify().replace("\r", "").replace("\n", "")
    return fulltext


def generate_document_id(url):
    document_id = re.findall(DOCUMENT_ID_RGX, url)[0].strip("/").replace("/", "-").upper()
    document_id = ":".join([DOCUMENT_ID_PREFIX, document_id]).upper().rstrip(".HTML").rstrip(".PDF").rstrip(".DOCX")
    return document_id
