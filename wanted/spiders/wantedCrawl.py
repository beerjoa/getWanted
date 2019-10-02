# -*- coding: utf-8 -*-

import scrapy
from wanted.items import WantedItem
import json
from scrapy_splash import *
import os

class WantedcrawlSpider(scrapy.Spider):
    name = 'wantedCrawl'
    allowed_domains = ['www.wanted.co.kr']
    # readline_test.py
    BASE_DIR = os.getcwd()
    f = open(BASE_DIR+"/userID.txt", 'r')
    uuid = f.readline()
    f.close()
    print(uuid)
    start_urls = ['https://www.wanted.co.kr/api/v4/jobs?1569934946091&country=kr&locations=all&jobSort=job.latest_order&years=-1&limit=20&offset=20']



    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                headers = {
                                        "referer": "https://www.wanted.co.kr/wdlist?country=kr&job_sort=job.latest_order&years=-1&locations=all",
                                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
                                        "wanted-user-agent": "user-web",
                                        "wanted-user-country": "KR",
                                        "wanted-user-language": "ko",
                                    },
                                cookies = {'uuid':self.uuid}
                            )


                                        
    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

    # yield SplashRequest("https://www.instagram.com/explore/tags/%ED%9E%90%EB%A7%81/", self.realRealParse,
    #         endpoint = 'render.html',
    #         args={'wait': 2.5}
    #     )
        for i in jsonresponse['data']:
            detailURL = "https://www.wanted.co.kr/wd/{}?referer_id={}".format(i['id'], i['company']['id'])
            yield scrapy.Request(detailURL, callback=self.detailParse,
                                    headers = {
                                        # "referer": "https://www.wanted.co.kr/wdlist?country=kr&job_sort=job.latest_order&years=-1&locations=all",
                                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
                                        "wanted-user-agent": "user-web",
                                        "wanted-user-country": "KR",
                                        "wanted-user-language": "ko",
                                    },
                                    # endpoint = 'render.html',
                                    # args={'wait': 2.5},
                                    meta = {
                                        'mainDic' : i,
                                    }
                                )

        next_page = jsonresponse['links']['next']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse,
                                    headers = {
                                        "referer": "https://www.wanted.co.kr/wdlist?country=kr&job_sort=job.latest_order&years=-1&locations=all",
                                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
                                        "wanted-user-agent": "user-web",
                                        "wanted-user-country": "KR",
                                        "wanted-user-language": "ko",
                                    }
                                )

    def detailParse(self, response):
        mainDic = response.meta['mainDic']
        js = response.selector.xpath('//script[contains(., "")]/text()').extract()
        jscleaned = eval(js[2])
        mainDic['title'] = jscleaned['title']
        mainDic['description'] = jscleaned['description']
        yield mainDic
