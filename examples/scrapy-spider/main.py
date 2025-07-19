import scrapy


class WebBotAuthSpider(scrapy.Spider):
    name = "web_bot_auth_spider"

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("DOWNLOADER_MIDDLEWARES", {
            "scrapy_spider.WebBotAuthMiddleware": 543,
        }, priority="spider")