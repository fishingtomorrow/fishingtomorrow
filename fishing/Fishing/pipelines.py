# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import uuid
    
class FishingPipeline(object):
    def process_item(self, item, spider):

        info = dict(item)
        if info.has_key('title') and info.has_key('meta') and info.has_key('article'):
            with codecs.open('d:/fishing/info/%s.json'%(uuid.uuid4()),'w','utf-8') as f:
                f.write(json.dumps(info, indent=4, sort_keys=True, ensure_ascii=False))
        
        return item
