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


class Diaoyur(BasePortiaSpider):
    name = "www.diaoyur.com"
    allowed_domains = [u'www.diaoyur.com']
    start_urls = [u'http://www.diaoyur.com/a/2018/35482.html']
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
                u'body',
                [
                    Field(
                        u'class0',
                        '.bread_wrapper > .bread_box > a:nth-child(2) *::text',
                        []),
                    Field(
                        u'class1',
                        '.bread_wrapper > .bread_box > a:nth-child(3) *::text',
                        []),
                    Field(
                        u'class2',
                        '.bread_wrapper > .bread_box > a:nth-child(4) *::text',
                        []),
                    Field(
                        u'title',
                        '.wrapper > .show_left > .show_title > h1 *::text',
                        []),
                    Field(
                        u'meta',
                        '.wrapper > .show_left > .show_title > span *::text',
                        []),
                    Field(
                        u'article',
                        '.wrapper > .show_left > .show_cnt *::text',
                        []),
                    Field(
                        u'up',
                        '.wrapper > .show_left > .big-share > .like-boring > dl > dd:nth-child(1) > .btn-like::attr(href)',
                        []),
                    Field(
                        u'down',
                        '.wrapper > .show_left > .big-share > .like-boring > dl > dd:nth-child(2) > .btn-boring::attr(href)',
                        [])]),
            Item(
                PortiaItem,
                None,
                u'body',
                [
                    Field(
                        u'class0',
                        '.bread_wrapper > .bread_box > a:nth-child(2)::attr(href)',
                        []),
                    Field(
                        u'class1',
                        '.bread_wrapper > .bread_box > a:nth-child(3)::attr(href)',
                        []),
                    Field(
                        u'title',
                        '.wrapper > .show_left > .show_title > h1 *::text',
                        []),
                    Field(
                        u'meta',
                        '.wrapper > .show_left > .show_title > span *::text',
                        []),
                    Field(
                        u'article',
                        '.wrapper > .show_left > .show_cnt *::text',
                        [])])]]
