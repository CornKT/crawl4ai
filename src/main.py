from fastapi import FastAPI
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from pydantic import BaseModel
import requests
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = FastAPI()


class URLItem(BaseModel):
    url: str


async def async_task():
    await asyncio.sleep(1)
    return "Async task completed"


async def crawl_task(url: str):
    async with AsyncWebCrawler(
        verbose=True,
        headless=True,
        use_persistent_context=True,
        # simulate_user=True,
        user_agent_mode="random",
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        },
    ) as crawler:
        result = await crawler.arun(
            url,
            js_code="window.scrollTo(0, 500); ",
            bypass_cache=True,
            delay_before_return_html=2,
            remove_overlay_elements=True,
            # html2text={"ignore_links": True},
            magic=True,
        )

        assert result.success, f"Failed to crawl {url}: {result.error_message}"
        print(f"Successfully crawled {url}")
        return result.markdown_v2


@app.get("/")
async def hello():
    return {"message": 'hello'}


@app.post("/crawl/")
async def crawl(url: URLItem):
    return {"result": await crawl_task(url.url)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
