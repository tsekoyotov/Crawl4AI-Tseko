import pytest
httpx = pytest.importorskip("httpx")
from httpx import AsyncClient, RequestError

from deploy.docker.server import app

class DummyCrawler:
    ready = True
    async def arun(self, url, config=None, dispatcher=None):
        raise RequestError("connection failed", request=None)
    async def arun_many(self, urls, config=None, dispatcher=None):
        raise RequestError("connection failed", request=None)

async def dummy_get_crawler(cfg):
    return DummyCrawler()

@pytest.mark.asyncio
async def test_crawl_invalid_domain_returns_502(monkeypatch):
    monkeypatch.setattr("deploy.docker.api.get_crawler", dummy_get_crawler)
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/crawl",
            json={
                "urls": ["https://bad-domain.invalid"],
                "browser_config": {},
                "crawler_config": {}
            },
        )
    assert response.status_code == 502
    assert "detail" in response.json()

