#!/usr/bin/env python3

import sys
print("Python path:", sys.path)

try:
    import scrapy_spider
    print(f"scrapy_spider imported successfully!")
    print(f"Version: {scrapy_spider.__version__}")
    print(f"WebBotAuthMiddleware available: {hasattr(scrapy_spider, 'WebBotAuthMiddleware')}")
    
    from scrapy_spider import WebBotAuthMiddleware
    print("WebBotAuthMiddleware imported successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
