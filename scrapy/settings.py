BOT_NAME = "car_scraper"

SPIDER_MODULES = ["car_scraper.spiders"]
NEWSPIDER_MODULE = "car_scraper.spiders"

COOKIES_ENABLED = True

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 2.5

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2.5
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'car_scraper.middlewares.HumanishDownloaderMiddleware': 400,
}

ITEM_PIPELINES = {
   "car_scraper.pipelines.DataValidationPipeline": 100,
   "car_scraper.pipelines.CustomImagePipeline": 200,
}

IMAGES_MIN_HEIGHT = 100
IMAGES_MIN_WIDTH = 100



REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
IMAGES_STORE = os.path.join(BASE_DIR, 'dataset')

FEEDS = {
    os.path.join(BASE_DIR, 'dataset', 'car_metadata.json'): {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'overwrite': True,
        'indent': 4,
    }
}
