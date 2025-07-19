"""
Scrapy Spider with Web Bot Authentication

An example project showing how to use web-bot-auth with Scrapy.
"""

from __future__ import annotations

__version__ = "0.1.0"

from typing import TYPE_CHECKING
import json

from scrapy import Request, Spider, signals
from scrapy.utils.url import url_is_from_any_domain
from web_bot_auth import BotAuth

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
        private_key = crawler.settings["WEB_BOT_AUTH_SIGNING_KEY"] or '{"kty":"OKP","crv":"Ed25519","kid":"poqkLGiymh_W0uP6PZFw-dvez3QJT5SolqXBCW38r0U","d":"n4Ni-HpISpVObnQMW0wOhCKROaIKqKtW_2ZYb2p9KcU","x":"JrQLj5P_89iXES9-vFgrIy29clF9CC_oPPsw3c5D0bs"}'
        cls.__wba = wb = BotAuth([json.loads(private_key)])
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider: Spider) -> None:
        None

    
    def process_request(
        self, request: Request, spider: Spider
    ) -> Request | Response | None:
        headers = self.__wba.get_bot_signature_header(request.url)
        request.headers.update(headers)
        return None

# Export the main class and version
__all__ = ["WebBotAuthMiddleware", "__version__"]
