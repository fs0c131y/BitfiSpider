# -*- coding: utf-8 -*-
import os
import errno
import scrapy


class ThebitfiSpider(scrapy.Spider):
    name = 'thebitfi'
    allowed_domains = ['bitfi.dev']
    start_urls = [
        'https://bitfi.dev/NoxMessages/Articles.aspx?Category=sources']

    def parse(self, response):
        if response.status == 200:
            files = response.xpath(
                '//*[contains(@class,"faq-section")]/a/@href')
            for file in files:
                url = 'https://bitfi.dev/NoxMessages/' + file.get()
                yield scrapy.Request(url, self.parse_file)

    def parse_file(self, response):
        if response.status == 200:
            #print(response.text)
            title = response.xpath('//*[contains(@class,"faq-section")]/h2/text()').get()
            subtitle = response.xpath('//*[contains(@class,"faq-section")]/h3/text()').get().rsplit('\\', 1)[0][1:].replace('\\', '/')
            code = response.xpath('//*[contains(@class,"faq-code")]/text()').extract()

            try:  
                os.makedirs('output/' + subtitle)
            except OSError as exc:
                pass

            with open('output/' + subtitle + '/' + title, 'a') as f:
                for line in code:
                    f.write(line + '\n')
