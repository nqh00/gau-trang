BOT_NAME = 'gautrang'
SPIDER_MODULES = ['gautrang.spiders']
NEWSPIDER_MODULE = 'gautrang.spiders'
SPLASH_URL = 'http://localhost:8050'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 5
LOG_LEVEL = 'CRITICAL'
USER_AGENT_LIST = "whatismybrowser-user-agents.txt"
SPIDER_MIDDLEWARES = { 'scrapy_splash.SplashDeduplicateArgsMiddleware': 100 }
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'random_useragent.RandomUserAgentMiddleware': 400 #pip install scrapy-random-useragent
}
ITEM_PIPELINES = {
   'gautrang.pipelines.gautrangPipeline': 300,
}