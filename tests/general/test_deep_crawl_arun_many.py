import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_parent_dir)

import os
import pytest
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy

@pytest.mark.asyncio
async def test_arun_many_deep_crawl_batch():
    html_path = os.path.join(os.path.dirname(__file__), '..', 'async', 'sample_wikipedia.html')
    url = f"file://{os.path.abspath(html_path)}"
    urls = [url, url]
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(max_depth=1, max_pages=1),
        cache_mode=CacheMode.BYPASS,
        stream=False,
    )
    async with AsyncWebCrawler(config=BrowserConfig(headless=True, verbose=False)) as crawler:
        results = await crawler.arun_many(urls=urls, config=config)
        assert len(results) == len(urls)
        assert all(r.success for r in results)

@pytest.mark.asyncio
async def test_arun_many_deep_crawl_stream():
    html_path = os.path.join(os.path.dirname(__file__), '..', 'async', 'sample_wikipedia.html')
    url = f"file://{os.path.abspath(html_path)}"
    urls = [url, url]
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(max_depth=1, max_pages=1),
        cache_mode=CacheMode.BYPASS,
        stream=True,
    )
    async with AsyncWebCrawler(config=BrowserConfig(headless=True, verbose=False)) as crawler:
        gen = await crawler.arun_many(urls=urls, config=config)
        collected = []
        async for result in gen:
            collected.append(result)
        assert len(collected) == len(urls)
        assert all(r.success for r in collected)
