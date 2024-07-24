import scrapy
from .base_spider import BaseAmazonSpider

class AmazonSpider(BaseAmazonSpider):
    name = 'amazon'
    
    def __init__(self, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        # Initialize the fetching of data from Google Sheets
        self.initialize_google_sheets()
    
    def start_requests(self):
        records = self.sheet.get_all_records()
        for index, record in enumerate(records, start=2):  # start=2 to account for header row and 1-based indexing
            url = record.get('Supplier link')
            if url and "amazon" in url:
                self.retries = 0
                self.processed_urls.add(url)
                yield scrapy.Request(url=url, callback=self.parse, meta={'row_number': index}, errback=self.handle_failure)