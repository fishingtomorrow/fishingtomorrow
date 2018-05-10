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


class BbsDiaoyu(BasePortiaSpider):
    name = "bbs.diaoyu.com"
    allowed_domains = [u'bbs.diaoyu.com']
    start_urls = [u'http://bbs.diaoyu.com/showtopic-608179-1-1.html']
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
                u'.main',
                [
                    Field(
                        u'head',
                        '.map *::text',
                        []),
                    Field(
                        u'title',
                        '.view-title > h1 *::text',
                        []),
                    Field(
                        u'meta',
                        '.main-left > .view-user-info *::text',
                        []),
                    Field(
                        u'key',
                        '.main-left > .view-article-property > .view-article-tag > p *::text',
                        []),
                    Field(
                        u'article',
                        '.main-left > .view-content *::text',
                        []),
                    Field(
                        u'comments',
                        '.main-left > .comment > .comment-list *::text',
                        [])])]]
