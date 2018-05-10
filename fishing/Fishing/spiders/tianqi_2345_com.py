from __future__ import absolute_import

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity
from scrapy.spiders import Rule

from ..utils.spiders import BasePortiaSpider
from ..utils.starturls import FeedGenerator, FragmentGenerator
from ..utils.processors import Item, Field, Text, Number, Price, Date, Url, Image, Regex
from ..items import PortiaItem


class Tianqi_2345(BasePortiaSpider):
    name = "tianqi.2345.com"
    allowed_domains = [u'tianqi.2345.com']
    start_urls = [u'http://tianqi.2345.com/wea_history/56294.htm']
    rules = [
        Rule(
            LinkExtractor(
                allow=('.*'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        )
    ]
    items = [[Item(PortiaItem,
                   None,
                   u'.module-data',
                   [Field(u'city',
                          '.btitle > h1 *::text',
                          []),
                       Field(u'year',
                             '.btitle > .posRt > .date-select-year > .field *::text',
                             []),
                       Field(u'month',
                             '.btitle > .posRt > .date-select-month > .field *::text',
                             []),
                       Field(u'info',
                             '.meta *::text',
                             []),
                       Field(u'field1',
                             '.meta *::text',
                             [])])]]
