import asyncio
import sys
from crawl4ai import AsyncWebCrawler, BrowserConfig
from playwright.async_api import Page, BrowserContext
from web_bot_auth import BotAuth


async def main():
    wb = BotAuth(
        [
            {
                "kty": "OKP",
                "crv": "Ed25519",
                "kid": "poqkLGiymh_W0uP6PZFw-dvez3QJT5SolqXBCW38r0U",
                "d": "n4Ni-HpISpVObnQMW0wOhCKROaIKqKtW_2ZYb2p9KcU",
                "x": "JrQLj5P_89iXES9-vFgrIy29clF9CC_oPPsw3c5D0bs",
            }
        ]
    )

    # 1) Configure the browser
    browser_config = BrowserConfig(headless=True, verbose=True)

    # 2) Create the crawler instance
    crawler = AsyncWebCrawler(config=browser_config)

    # 3) Define the Hook
    async def before_goto(page: Page, context: BrowserContext, url: str, **kwargs):
        # Called before navigating to each URL.
        print(f"[HOOK] before_goto - About to navigate: {url}")

        headers = wb.get_bot_signature_header(url)
        await page.set_extra_http_headers(headers)

        return page

    # 4) Attach the Hook
    crawler.crawler_strategy.set_hook("before_goto", before_goto)

    await crawler.start()

    # 5) Run the crawler on an example page
    # use the command line argument to specify the URL
    args = sys.argv[1:]
    url = args[0]
    result = await crawler.arun(url)

    if result.success:
        print("\nCrawled URL:", result.url)
        print("Response", result.html)
    else:
        print("Error:", result.error_message)

    await crawler.close()


if __name__ == "__main__":
    asyncio.run(main())
