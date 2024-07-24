import scrapy
from .base_spider import BaseAmazonSpider

class AmazonRetrySpider(BaseAmazonSpider):
    name = 'amazon_retry'
    
    def __init__(self, *args, **kwargs):
        super(AmazonRetrySpider, self).__init__(*args, **kwargs)
        # Initialize the fetching of data from Google Sheets
        self.initialize_google_sheets()
    
    def start_requests(self):
        records = self.sheet.get_all_records()
        for index, record in enumerate(records, start=2):  # start=2 to account for header row and 1-based indexing
            url = record.get('Supplier link')
            scraping_remarks = record.get('Scraping Remarks')
            if url and (not scraping_remarks or 'No data captured' in scraping_remarks or 'No Quantity' in scraping_remarks or 'No Price' in scraping_remarks) and "amazon" in url:
                self.retries = 0
                self.processed_urls.add(url)
                yield scrapy.Request(url=url, callback=self.parse, meta={'row_number': index}, errback=self.handle_failure)