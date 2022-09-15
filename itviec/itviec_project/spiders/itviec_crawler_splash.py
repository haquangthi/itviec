# -*- coding: utf-8 -*-
import base64
from pydoc import resolve
import scrapy
from itviec.items import ItviecItem
from scrapy_splash import SplashRequest
import re

class WebsosanhSpider(scrapy.Spider):

    # name = "itviec"
    allowed_domains = ['itviec.com']
    start_urls = ["https://itviec.com/it-jobs?page=4&query=&source=search_job"]   
    
    script = """
        function main(splash)
            --assert(splash:autoload("https://code.jquery.com/jquery-3.1.1.min.js"))
            local url = splash.args.url
            local content = splash.args.content
            --assert(splash:set_content(content, "text/html; charset=utf-8", url))
            assert(splash:go(url))
            assert(splash:wait(2))
            --local scroll_to = splash:jsfunc("window.scrollTo")
            --scroll_to(0, 1400)
            assert(splash:wait(2))
            assert(splash:select('#jobs > div.search-page__jobs-pagination > ul > li:last-child >a'))
            local element = splash:select('#jobs > div.search-page__jobs-pagination > ul > li:last-child >a')
            local bounds = element:bounds()
            assert(element:mouse_click{x=bounds.width/3, y=bounds.height/3})

            assert(splash:runjs('document.querySelector("#jobs > div.search-page__jobs-pagination > ul > li:last-child >a").click()')) 
            --local button = splash:select('#jobs > div.search-page__jobs-pagination > ul > li:last-child >a')
            --button:mouse_click()    
            return {
                html = splash:html(),
                url = splash:url(),
                splash:set_viewport_full(),
                png = splash:png(),

            }
        end
        """
    script_screenshot = """
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(2))
            local scroll_to = splash:jsfunc("window.scrollTo")
            scroll_to(0, 1400)
            assert(splash:wait(2))
            local element = splash:select('#jobs > div.search-page__jobs-pagination > ul > li:last-child >a')
            local bounds = element:bounds()
            assert(element:mouse_click{x=bounds.width, y=bounds.height})
            return {
                html = splash:html(),
                splash:set_viewport_full(),
                png = splash:png(),                
                har = splash:har(),
            }
            end
    """
    def start_requests(self):       
        for url in self.start_urls:
            yield SplashRequest(url, endpoint="execute", callback=self.parse,meta={
                'splash':{"endpoint": "execute", "args": {"lua_source": self.script_screenshot}},
                'page':1,
            })


    def parse(self, response):
        
        page = response.meta['page']        
        # print(response.body)
        # itviec_html = "itviec.html"
        # with open(itviec_html, 'wb') as f:
        #     f.write(response.body)

        imgdata = base64.b64decode(response.data['png'])
        
        filename = "screenshoot{}.png".format(page)
        with open(filename, 'wb') as f:
            f.write(imgdata)
        print("====================")
        print(f" Request page {page+1}")
        print ("\n----------------")
        yield SplashRequest(
            url=response.url,
            callback=self.parse,
            dont_filter = True,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}},
                'page': int(page) + 1,
                'content':response.text
            },
        )