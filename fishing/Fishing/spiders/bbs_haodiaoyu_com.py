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


class BbsHaodiaoyu(BasePortiaSpider):
    name = "bbs.haodiaoyu.com"
    allowed_domains = [u'bbs.haodiaoyu.com']
    start_urls = [u'http://bbs.haodiaoyu.com/thread-199150-1-1.html']
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
    items = [
        [
            Item(
                PortiaItem,
                None,
                u'#postlist',
                [
                    Field(
                        u'class',
                        'table:nth-child(1) > tr > .plc > .bm *::text',
                        []),
                    Field(
                        u'title',
                        'div:nth-child(3) > .plhin > tr:nth-child(1) > .plc > .cl > .cl > .ts > span *::text',
                        []),
                    Field(
                        u'meta',
                        'div:nth-child(3) > .plhin > tr:nth-child(1) > .plc > .pi > .pti > .authi > .avt_right > .tops *::text',
                        []),
                    Field(
                        u'hot',
                        'div:nth-child(3) > .plhin > tr:nth-child(1) > .plc > .pi > .pti > .authi > .avt_right > .post_date *::text',
                        []),
                    Field(
                        u'stat',
                        'div:nth-child(3) > .plhin > tr:nth-child(1) > .plc > .pi > .pti > .authi > .avt_right > .pct > .pcb > .pcbs > .thread-info *::text',
                        []),
                    Field(
                        u'article',
                        'div:nth-child(3) > .plhin > tr:nth-child(1) > .plc > .pi > .pti > .authi > .avt_right > .pct > .pcb > .pcbs > table > tr > .t_f *::text',
                        [])])]]
