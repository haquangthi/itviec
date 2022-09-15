# -*- coding: utf-8 -*-
import scrapy
from itviec.items import ItviecItem
import re
import time
from datetime import datetime
from datetime import timedelta

class WebItviec(scrapy.Spider):

    name = "itviec"
    allowed_domains = ['itviec.com']
    base_url = "https://itviec.com/{}"
    start_urls = ["https://itviec.com/it-jobs?page=1&query=&source=search_job"]       
    page_url = "https://itviec.com/it-jobs?page={}&query=&source=search_job"
    
    def start_requests(self):       
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.get_list_work, 
            meta={
                'page': 1
            })

    def get_list_work(self, response):
       list_jobs = response.xpath("//*[@class='first-group']/div")
       for job in list_jobs:
            province = "".join(job.xpath("//*[@class='first-group']/div//*[contains(@class, 'address')]//text()").extract())
            url = self.base_url.format(job.xpath(".//*[contains(@class, 'title')]//a/@href").extract_first())

            yield scrapy.Request(url, self.extract_detail, meta={
                "province": province,
            })            
                   
    #    if list_jobs:
    #        next_page = int(response.meta['page']) + 1
    #        print(self.page_url.format(next_page))
    #        time.sleep(3)
    #        yield scrapy.Request(self.page_url.format(next_page), callback=self.get_list_work, meta={
    #            'page': next_page
    #        })

    def cal_data_date(self, data_date):
        if 'd' in data_date:
            day = data_date.replace('d').strip()
            data_date = datetime.today() - timedelta(days=day)
            return data_date
        else:
            return datetime.today()
    
    def extract_detail(self, response):
        item = ItviecItem()
        # item["province"] = response.meta['province']
        item["url"] = response.url
        item["company_name"] = response.xpath("//*[contains(@class, 'employer-long-overview__name')]//*/text()").extract_first().replace("\t", "").replace("\n", "")
        item["address"] = response.xpath("//*[contains(@class, 'job-details__overview')]//*[contains(@class, 'svg-icon__text')]/span[following-sibling::a]/text()").extract_first().replace("\t", "").replace("\n", "")
        item["day_work"] = response.xpath("//*[contains(@class, 'employer-long-overview__basic')]/*[3]/*[2]/text()").extract_first().replace("\t", "").replace("\n", "")
        item["country"] = response.xpath("//*[contains(@class, 'employer-long-overview__basic')]/*[5]/*[2]/text()").extract_first().replace("\t", "").replace("\n", "")
        item["no_employee"] = response.xpath("//*[contains(@class, 'employer-long-overview__basic')]/*[2]/*[2]/text()").extract_first().replace("\t", "").replace("\n", "")
        item["job_title"] = response.xpath("//div[contains(@class, job-details__header)]/*[contains(@class, 'job-details__title')]/text()").extract_first().replace("\t", "").replace("\n", "")        
        item["job_skill"] = "".join(response.xpath("(//h2[contains(.,'Skills and Experience')]/following-sibling::div)[1]//text()").extract()).replace("\t", "").replace("\n", "")
        item["job_description"] = "".join(response.xpath("(//h2[contains(.,'Job Description')]/following-sibling::div)[1]//text()").extract()).replace("\t", "").replace("\n", "")
        item["data_date"] = self.cal_data_date(response.xpath("//*[contains(@class, 'distance-time')]//*/text()").extract_first().replace("\t", "").replace("\n", ""))
        item["crawl_date"] = datetime.today()
        print(item)





