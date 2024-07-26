# spiders/amazon_spider.py

import scrapy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime
from ..items import AmazonItem
from dateutil.parser import parse
from scrapy.http import Request
import re
import os

class BaseAmazonSpider(scrapy.Spider):
    
    def __init__(self, *args, **kwargs):
        super(BaseAmazonSpider, self).__init__(*args, **kwargs)
        
    def initialize_google_sheets(self):
         # Load configuration
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, '..', '..', 'config.json')
        
        
        with open(config_path) as config_file:
            config = json.load(config_file)
        
        credentials_path = os.path.join(base_dir, '..', '..',config['credentials_path'])
        self.spreadsheet_id = config['spreadsheet_id']
        self.sheet_name = config['daily_upload_sheet_name']
        
        # Authenticate and connect to Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(self.spreadsheet_id).worksheet(self.sheet_name)
        
        # Store scraped data in memory
        self.scraped_data = []
        self.processed_urls = set()
        
        self.retries = 0
        self.max_retries = 3

    # def start_requests(self):
    #     records = self.sheet.get_all_records()
    #     for index, record in enumerate(records, start=2):  # start=2 to account for header row and 1-based indexing
    #         url = record.get('Supplier link')
    #         if url and "amazon" in url:
    #             self.retries = 0
    #             self.processed_urls.add(url)
    #             yield scrapy.Request(url=url, callback=self.parse, meta={'row_number': index}, errback=self.handle_failure)

    def parse(self, response):
        items = AmazonItem()
        
        # Extract the product title from the span element with id "productTitle"
        product_name = response.xpath('//span[@id="productTitle"]/text()').get()
        if product_name:
            product_name = product_name.strip()
        
        # Extract the price components
        price_whole = response.xpath('//span[@class="a-price-whole"]/text()').get()
        price_fraction = response.xpath('//span[@class="a-price-fraction"]/text()').get()
        
        # Combine the whole and fractional parts of the price
        if price_whole and price_fraction:
            price = f"{price_whole}.{price_fraction}"
        else:
            price = None
        
        # Extract the "Currently unavailable" text or the quantity available
        quantity = response.xpath('//div[@id="availability"]//span/text()').re_first(r'Currently unavailable')
        if not quantity:
            quantity = response.xpath('//div[@id="availability"]//span/text()').get()
            if quantity:
                quantity = quantity.strip()
                
        delivery_date_raw = response.xpath('//span[contains(@data-csa-c-delivery-time, "")]/span[@class="a-text-bold"]/text()').get()
        delivery_date = None
        days_delivered = None
        if delivery_date_raw:
            delivery_date = delivery_date_raw.strip()
            
            # compute for the number of days it can be deliver
            days_delivered = self.calculate_delivery_date(delivery_date_raw.strip())
            
        
        # Check for "Currently unavailable" in a different location
        if not quantity:
            quantity = response.xpath('//div[@id="outOfStock"]//span/text()').get()

        # Add to scraped data
        row_number = response.meta['row_number']
        # if not (product_name and (price_whole or price_fraction) and quantity):
        if not (product_name or price_whole or price_fraction or quantity):
            if self.retries <= self.max_retries:
                self.retries += 1
                self.logger.info(f"Retrying {response.url} due to missing data.")
                print(f'------------------------Retries : {self.retries}--------------------------------')
                yield Request(response.url, callback=self.parse, meta={'row_number': row_number}, errback=self.handle_failure, dont_filter=True)
            else:
                self.logger.info(f"Max retries reached for {response.url}. Saving blank results.")
                self.scraped_data.append({
                    'row_number': row_number,
                    'remarks': f'No data captured'
                })
        else:
            items['product_name'] = product_name
            items['price'] = price
            items['quantity'] = quantity
            items['delivery_date'] = delivery_date
            items['days_delivered'] = days_delivered

            self.scraped_data.append({
                'row_number': row_number,
                'product_name': product_name,
                'price': price,
                'quantity': quantity,
                'delivery_date': delivery_date,
                'days_delivered': days_delivered
            })

            yield items
        
    def parse_delivery_date(self, date_str):
        """Parse delivery date considering different possible formats in Dutch and English."""
        try:
            parsed_date = parse(date_str, dayfirst=True)
            return parsed_date.strftime('%m/%d/%Y')
        except ValueError:
            return None
        
    def handle_failure(self, failure):
        row_number = failure.request.meta['row_number']
        self.scraped_data.append({
            'row_number': row_number,
            'remarks': 'Request failed',
        })
        self.logger.error(f'Request failed for row {row_number}: {failure.value}')

    def get_remarks(self, data):
        remarks = []

        if data['price'] is None:
            remarks.append("No Price has been captured")
        else:
            remarks.append("Price has been updated")

        if data['quantity'] is None:
            remarks.append("No Quantity has been captured")
        else:
            remarks.append("Quantity has been updated")

        return " | ".join(remarks)
    
    def translate_dutch_date(self,date_str):
        # Mapping of Dutch month names to English month names
        dutch_months = {
            "januari": "January", "februari": "February", "maart": "March",
            "april": "April", "mei": "May", "juni": "June",
            "juli": "July", "augustus": "August", "september": "September",
            "oktober": "October", "november": "November", "december": "December"
        }
        for dutch, english in dutch_months.items():
            date_str = date_str.replace(dutch, english)
        return date_str

    def calculate_delivery_date(self,date_str):
        """Calculate delivery date considering different possible formats."""
        try:
            # Handle "tomorrow" and "morgen" cases
            if 'tomorrow' in date_str.lower() or 'morgen' in date_str.lower():
                return 1
            else:
                # Translate Dutch date to English
                date_str = self.translate_dutch_date(date_str)
                
                # Extract date part from the string
                date_pattern = r'\d{1,2} \w+ \d{4}|\d{1,2} \w+|\w+, \d{1,2} \w+, \d{4}'
                date_part = re.search(date_pattern, date_str.lower())
                if date_part:
                    date_part = date_part.group()
                    parsed_date = parse(date_part, dayfirst=True).date()
                    return (parsed_date - datetime.today().date()).days
                else:
                    return None
        except ValueError as e:
            print(e)
            return None

    def close(self, reason):
        print(self.scraped_data)
        headers = self.sheet.row_values(1)
        title_col = self.sheet.find('Amazon Title').col if 'Amazon Title' in headers else None
        price_col = self.sheet.find('Amazon Price').col if 'Amazon Price' in headers else None
        quantity_col = self.sheet.find('Stock Status').col if 'Stock Status' in headers else None
        remarks_col = self.sheet.find('Scraping Remarks').col if 'Scraping Remarks' in headers else None
        delivery_date_col = self.sheet.find('Amazon Delivery Date').col if 'Amazon Delivery Date' in headers else None
        days_delivered_col = self.sheet.find('Amazon Delivery Day').col if 'Amazon Delivery Day' in headers else None

        cell_updates = []

        for data in self.scraped_data:
            row_number = data['row_number']
            if 'remarks' in data and remarks_col:
                cell_updates.append({'range': f'{chr(64+remarks_col)}{row_number}', 'values': [[data['remarks']]]})
            else:
                if title_col and [data['product_name']]:
                    cell_updates.append({'range': f'{chr(64+title_col)}{row_number}', 'values': [[data['product_name']]]})
                if price_col and [data['price']]:   
                    cell_updates.append({'range': f'{chr(64+price_col)}{row_number}', 'values': [[data['price']]]})
                if quantity_col and [data['quantity']]:
                    cell_updates.append({'range': f'{chr(64+quantity_col)}{row_number}', 'values': [[data['quantity']]]})
                if delivery_date_col and [data['delivery_date']]:
                    cell_updates.append({'range': f'{chr(64+delivery_date_col)}{row_number}', 'values': [[data['delivery_date']]]})
                if delivery_date_col and [data['delivery_date']]:
                    cell_updates.append({'range': f'{chr(64+days_delivered_col)}{row_number}', 'values': [[data['days_delivered']]]})
                if remarks_col:
                    cell_updates.append({'range': f'{chr(64+remarks_col)}{row_number}', 'values': [[self.get_remarks(data)]]})

        # Batch update cells to reduce the number of API calls
        if cell_updates:
            self.sheet.batch_update(cell_updates)
