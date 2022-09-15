# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class ItviecPipeline:
    def open_spider(self, spider):
        hostname = '127.0.0.1'
        port='5432'
        username = 'postgres'
        password = 'admin'
        database = 'demo'
        self.connection = psycopg2.connect(host=hostname, port=port, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()
    
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.cur.execute('''INSERT INTO test.itviec(company_name, day_work, country, no_employee, job_title, job_skill, job_description, url, address, data_date, crawl_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (item.get('company_name', None), item.get('day_work', None), item.get('country', None), item.get('no_employee',None),item.get('job_title', None), item.get('job_skill', None), item.get('job_description', None), item.get('url', None), item.get('address', None), item.get('data_date', None), item.get('crawl_date', None)))
            self.connection.commit()
        except psycopg2.IntegrityError:
            self.conn.rollback()
            raise
        return item

