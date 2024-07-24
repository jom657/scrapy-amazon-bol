from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from pydispatch import dispatcher
from amazon.spiders.amazon_spider import AmazonSpider
from amazon.spiders.retry_spider import AmazonRetrySpider

# Get the project settings
settings = get_project_settings()

# Create a CrawlerProcess with the settings
process = CrawlerProcess(settings)

# Flag to check if AmazonSpider has finished
amazon_spider_finished = False

# Function to run AmazonRetrySpider after AmazonSpider has finished
def spider_closed(spider, reason):
    global amazon_spider_finished
    if spider.name == 'amazon':
        amazon_spider_finished = True
        print('---------------------------------- Running Retry Spider ---------------------------------')
        process.crawl(AmazonRetrySpider)
        process.start()  # Start the crawling process for the retry spider

# Connect the signal to the function
dispatcher.connect(spider_closed, signal=signals.spider_closed)

# Schedule the AmazonSpider
print('---------------------------------- Running Amazon Spider ---------------------------------')
process.crawl(AmazonSpider)

# Start the crawling process
process.start()
