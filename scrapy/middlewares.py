

from scrapy import signals
from itemadapter import ItemAdapter
import random
from urllib.parse import urlparse


class carScraperSpiderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        
        return None

    def process_spider_output(self, response, result, spider):
       
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
       
        pass

    async def process_start(self, start):
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class HumanishDownloaderMiddleware:
    def __init__(self):
        self.profiles = [
            {
                "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "hints": {
                    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"'
                }
            },
            {
                "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
                "hints": {
                    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"'
                }
            },
            {
                "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "hints": {
                    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"macOS"'
                }
            },
            {
                "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
                "hints": {}  # Safari has no client hints by default
            },
            {
                "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
                "hints": {}  # Firefox has no client hints by default
            }
        ]
        
        self.chosen_profile = random.choice(self.profiles)

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
      
        request.headers['User-Agent'] = self.chosen_profile['ua']

    
        for hint_name, hint_val in self.chosen_profile['hints'].items():
            request.headers[hint_name] = hint_val

       
        url_lower = request.url.lower()
        is_image = any(ext in url_lower for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']) or 'csphoto' in url_lower

        if is_image:
            request.headers['Accept'] = 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
            request.headers['Sec-Fetch-Dest'] = 'image'
            request.headers['Sec-Fetch-Mode'] = 'no-cors'
        else:
            request.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
            request.headers['Sec-Fetch-Dest'] = 'document'
            request.headers['Sec-Fetch-Mode'] = 'navigate'
            request.headers['Sec-Fetch-User'] = '?1'

        
        request.headers['Accept-Language'] = 'ja,en-US;q=0.9,en;q=0.8'
        request.headers['Accept-Encoding'] = 'gzip, deflate, br'
        request.headers['Upgrade-Insecure-Requests'] = '1'

   
        req_domain = urlparse(request.url).netloc
        referer = request.headers.get('Referer', b'').decode('utf-8', errors='ignore')
        if referer:
            ref_domain = urlparse(referer).netloc
            if req_domain == ref_domain:
                request.headers['Sec-Fetch-Site'] = 'same-origin'
            elif req_domain.endswith(ref_domain) or ref_domain.endswith(req_domain):
                request.headers['Sec-Fetch-Site'] = 'same-site'
            else:
                request.headers['Sec-Fetch-Site'] = 'cross-site'
        else:
            request.headers['Sec-Fetch-Site'] = 'none'

        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name} | Using browser UA: {self.chosen_profile['ua']}")
