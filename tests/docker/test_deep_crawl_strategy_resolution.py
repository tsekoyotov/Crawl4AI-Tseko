from crawl4ai.async_configs import CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy


def test_init_resolves_strategy_from_string():
    config = CrawlerRunConfig(deep_crawl_strategy="BFSDeepCrawlStrategy")
    assert isinstance(config.deep_crawl_strategy, BFSDeepCrawlStrategy)


def test_from_kwargs_resolves_strategy_from_string():
    config = CrawlerRunConfig.from_kwargs({"deep_crawl_strategy": "BFSDeepCrawlStrategy"})
    assert isinstance(config.deep_crawl_strategy, BFSDeepCrawlStrategy)
