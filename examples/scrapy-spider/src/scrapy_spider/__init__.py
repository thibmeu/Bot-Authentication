from __future__ import annotations

"""
Scrapy Spider with Web Bot Authentication

An example project showing how to use web-bot-auth with Scrapy.
"""

import web_bot_auth

__version__ = "0.1.0"

from typing import TYPE_CHECKING

from scrapy import Request, Spider, signals
from scrapy.utils.url import url_is_from_any_domain

if TYPE_CHECKING:
    # typing.Self requires Python 3.11
    from typing_extensions import Self

    from scrapy.crawler import Crawler
    from scrapy.http import Response


class WebBotAuthMiddleware:
    """Set Basic HTTP Authorization header
    (http_user and http_pass spider class attributes)"""

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> Self:
        o = cls()
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider: Spider) -> None:
        usr = getattr(spider, "http_user", "")
        pwd = getattr(spider, "http_pass", "")
        if usr or pwd:
            self.domain = spider.http_auth_domain  # type: ignore[attr-defined]

    def process_request(
        self, request: Request, spider: Spider
    ) -> Request | Response | None:
        auth = getattr(self, "auth", None)
        if (
            auth
            and b"Authorization" not in request.headers
            and (not self.domain or url_is_from_any_domain(request.url, [self.domain]))
        ):
            request.headers[b"Authorization"] = auth
        return None

# Export the main class and version
__all__ = ["WebBotAuthMiddleware", "__version__"]
