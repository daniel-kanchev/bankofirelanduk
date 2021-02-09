import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bankofirelanduk.items import Article


class IrelandukSpider(scrapy.Spider):
    name = 'irelanduk'
    start_urls = ['https://www.bankofirelanduk.com/about/media-centre/blog/']

    def parse(self, response):
        links = response.xpath('//a[@role="button"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1[@class="entry-title"]/text()').get().strip()
        content = response.xpath('//div[@class="entry-content"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
