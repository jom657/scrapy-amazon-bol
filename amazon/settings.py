# Scrapy settings for amazon project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "amazon"

SPIDER_MODULES = ["amazon.spiders"]
NEWSPIDER_MODULE = "amazon.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "amazon (+http://www.yourdomain.com)"
# USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.105 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True



# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8
COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "amazon.middlewares.AmazonSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "amazon.middlewares.AmazonDownloaderMiddleware": 543,
#}

# Proxy IP pool
# DOWNLOADER_MIDDLEWARES = {
#     # ...
#     'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
#     'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
#     # ...
# }

# PROXY_POOL_ENABLED = True
# ROTATED_PROXY_ENABLED = True

# ROTATING_PROXY_LIST_PATH = 'proxies.txt'

# User Agents

# # -------------------------- SCRAPEOPS--------------------------------------
# DOWNLOADER_MIDDLEWARES = {
#     # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 300,
#     # 'rotating_proxies.middlewares.BanDetectionMiddleware': 301,
#     # 'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
#     # 'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
#     'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
# }


# SCRAPEOPS_API_KEY = '5006d5f2-32ec-4721-9978-39a2f4412d75'
# SCRAPEOPS_PROXY_ENABLED = True
# # -----------------------------------------------------------------------------


# # ----------------------DATAIMPULSE ROTATING PROXY--------------------------
# PROXY_USER = 'e5fe3817f8fbbf605fd1'
# PROXY_PASSWORD = 'd02b51b7be148291'
# PROXY_URL = 'gw.dataimpulse.com'
# PROXY_PORT = '823'

# # RETRY_TIMES = 3  # Number of times to retry
# # RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]  # HTTP codes to retry

# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
#     'amazon.middlewares.BookProxyMiddleware': 120,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 100,
# }
# # -------------------------------------------------------------------------

# ---------------------Custom Rotating Proxies from Webshsare---------------
# DOWNLOADER_MIDDLEWARES = {
#     'amazon.middlewares.CustomRotatingProxyMiddleware': 120,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 100,
# }

DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # 'amazon.middlewares.CustomRetryMiddleware': 550,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'amazon.middlewares.CustomProxyMiddleware': 120,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 100,
}
RETRY_TIMES = 3  # Number of times to retry
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]  # HTTP codes to retry

# ---------------------------------------------------------------------------

# # ----------------- Custom Rotating proxy Middleware--------------
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
#     'amazon.middlewares.CustomProxyMiddleware': 100,
# }

# # Optional: Use random user agents to reduce detection risk
# RANDOM_UA_PER_PROXY = True
# # -----------------------------------------------------------------


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "amazon.pipelines.AmazonPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# # Enable Retry Middleware
# RETRY_ENABLED = True

# # Set the maximum number of retries
# RETRY_TIMES = 5  # You can adjust this number as needed

# # Set the HTTP status codes to be retried
# RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

# # Optional: Set a custom retry delay to avoid immediate retries
# RETRY_WAIT = 10  # Wait 10 seconds before retrying

# Set settings whose default value is deprecated to a future-proof value
# REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
# FEED_EXPORT_ENCODING = "utf-8"
