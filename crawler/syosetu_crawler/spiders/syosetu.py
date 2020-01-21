# -*- coding: utf-8 -*-
import scrapy
import json
import os

class SyosetuSpider(scrapy.Spider):
    name = 'syosetu'
    allowed_domains = ['ncode.syosetu.com']
    current = 0
    def start_requests(self):
        with open('ncodes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        ncodes = data['2004']
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
        if os.path.exists('novels/%s'%ncode) == False:
            os.mkdir('novels/%s'%ncode)
        
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
        
            
