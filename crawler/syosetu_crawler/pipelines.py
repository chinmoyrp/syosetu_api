# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SyosetuWriterPipeline(object):   
    def open_spider(self, spider):
        #self.html = open('n174ct.html', 'w', encoding='utf-8')
    
    def close_spider(self, spider):
        #self.html.close()
    
    def process_item(self, item, spider):
        #self.html.write(item['title'])
        #self.html.write(item['author'])
        #self.html.write(item['summary'])
        #for c in item['chapters']:
            #self.html.write(c)
        return item
