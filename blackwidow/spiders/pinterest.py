from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

from blackwidow.items import HeelsItem


class PinterestSpider(CrawlSpider):

    name = 'pinterest'
    allowed_domains = ['pinterest.com', ]
    start_urls = [
        'http://pinterest.com/vintalines/likes/',
    ]

    rules = (
        # find detail page then parse it
        Rule(
            SgmlLinkExtractor(
                allow=(r'pin/\d+/$', ),  # http://pinterest.com/pin/128141551870912604/
                unique=True,
            ),
            callback='parse_pin_detail',
        ),
    )

    def parse_pin_detail(self, response):
        hxs = HtmlXPathSelector(response)

        item = HeelsItem()

        item['comment'] = hxs.select('//title/text()').extract()

        urls_1 = hxs.select('//div[contains(@class, "pinWrapper")]//div[contains(@class, "pinImageSourceWrapper")]//img/@src').extract()
        urls_2 = hxs.select('//div[contains(@class, "pinWrapper")]//div[contains(@class, "pinImageSourceWrapper")]//a/@href').extract()
        item['image_urls'] = urls_1 + urls_2

        item['source_url'] = response.url

        return item
