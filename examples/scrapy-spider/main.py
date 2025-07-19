import scrapy
from scrapy_spider import WebBotAuthMiddleware

class WebBotAuthSpider(scrapy.Spider):
    name = "web_bot_auth_spider"
    start_urls = ['https://http-message-signatures-example.research.cloudflare.com/debug']

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("DOWNLOADER_MIDDLEWARES", {
            "scrapy_spider.WebBotAuthMiddleware": 543,
        }, priority="spider")
    
    def parse(self, response):
        self.logger.info("Response received: %s", response.status)
        self.logger.info("Headers sent: %s", response.request.headers)
        yield {
            'url': response.url,
            'status': response.status,
            'headers': dict(response.request.headers),
        }