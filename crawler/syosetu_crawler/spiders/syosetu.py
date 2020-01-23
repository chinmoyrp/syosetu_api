# -*- coding: utf-8 -*-
import scrapy
import json
import os

class SyosetuSpider(scrapy.Spider):
    name = 'syosetu'
    allowed_domains = ['ncode.syosetu.com']
    current = 0
    key = None
    json=None
    
    def __init__(self, key=None, json=None, *args, **kwargs):
        super(SyosetuSpider, self).__init__(*args, **kwargs)
        self.key = key
        self.json = json
        
    def start_requests(self):
        with open(str(self.json), 'r', encoding='utf-8') as f:
            data = json.load(f)
        key = str(self.key)
        self.log("###################KEY = %s\t JSON=%s"%(key, self.json))
        ncodes = data[key]
        self.count = len(ncodes)
        self.log("Found %d novels"%self.count)
        for ncode in ncodes:
            url = 'http://ncode.syosetu.com/{}'.format(ncode)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.current += 1
        ncode = response.url.split('/')[-1]
        self.log("Processing %s \t %d/%d"%(ncode, self.current, self.count))
        if os.path.exists('novels') == False:
            os.mkdir('novels')
        if os.path.exists('novels/%s.%s'%(ncode, self.key)) == False:
            os.mkdir('novels/%s.%s'%(ncode, self.key))
        
        title = response.css('p.novel_title').get()
        author = response.css('div.novel_writername').get()
        summary = response.css('div#novel_ex').get()
        index = response.css('div.index_box').get()
        
        with open('novels/%s/%s.html'%(ncode,ncode), 'w', encoding='utf-8') as f:
            data = ""
            if summary != None and index != None:
                data = '\n'.join([title, author, summary, index])
            else:
                content = '\n'.join(response.css('div.novel_view').getall())
                data = '\n'.join([title, author, content])
            f.write(data)
                
        self.log("Written index for %s" % ncode)
        
        for href in response.css('dd.subtitle a::attr(href)').getall():
            yield response.follow(href, self.parse_chapters)
        
    def parse_chapters(self, response):
        split = response.url.rstrip('/').split('/')
        chapter = split[-1]
        ncode = split[-2]
        idx = response.css('div#novel_no').get()
        subtitle = response.css('p.novel_subtitle').get()
        content = '\n'.join(response.css('div.novel_view').getall())
        
        with open('novels/%s/%s.html'%(ncode,chapter), 'w', encoding='utf-8') as f:
            data = '\n'.join([idx, subtitle, content])
            f.write(data)
        self.log("Written chapter %s/%s \t (novel: %d/%d)"%(chapter, idx.split('/')[1], self.current, self.count))
        
            
