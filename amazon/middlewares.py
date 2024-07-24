# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import logging


class AmazonSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class AmazonDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
        
        

class CustomProxyMiddleware:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        with open('proxies.txt', 'r') as f:
            proxy_list = [line.strip() for line in f]
        middleware = cls(proxy_list)
        return middleware

    def process_request(self, request, spider):
        proxy = random.choice(self.proxy_list)
        request.meta['proxy'] = f"http://{proxy}"
        
        
class BookProxyMiddleware(object):
   @classmethod
   def from_crawler(cls, crawler):
       return cls(crawler.settings)
 
   def __init__(self, settings):
       self.username = settings.get('PROXY_USER')
       self.password = settings.get('PROXY_PASSWORD')
       self.url = settings.get('PROXY_URL')
       self.port = settings.get('PROXY_PORT')
 
   def process_request(self, request, spider):
       host = f'http://{self.username}:{self.password}@{self.url}:{self.port}'
       request.meta['proxy'] = host
       
       
class CustomRetryMiddleware(RetryMiddleware):

    def __init__(self, settings):
        super().__init__(settings)
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))

    def process_response(self, request, response, spider):
        if self._needs_retry(request, response):
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def _needs_retry(self, request, response):
        # Check if response is empty or missing expected data
        if response.status in self.retry_http_codes:
            return True

        product_name = response.css('#productTitle::text').get()
        price_whole = response.css('.a-price-whole::text').get()
        price_fraction = response.css('.a-price-fraction::text').get()
        quantity = response.css('#availability span::text').re_first(r'Currently unavailable')

        if not (product_name and (price_whole or price_fraction) and quantity):
            logging.info(f"------------ Retrying {request.url} due to missing data.")
            return True

        return False
