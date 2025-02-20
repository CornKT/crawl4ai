from fastapi import FastAPI
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
import requests


async def test():
    request = {
        "urls": "https://www.zoopla.co.uk/for-sale/details/69117958/?search_identifier=789715c86a8096916567c9304f6855f82e6d66b34a9be63fd28d14a80b5b81a9&weekly_featured=1&utm_content=featured_listing",
        "crawler_params": {
            "override_navigator": True,
            "magic": True,
            "bypass_cache": True,
            "use_persistent_context": True,
            "chrome_channel": "chrome",
            "delay_before_return_html": 5.0,
            "headers": {
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
        },
    }
    headers = {"Authorization": "Bearer trinhtit2003"}
    response = requests.post(
        "http://localhost:11235/crawl", headers=headers, json=request
    )
    task_id = response.json()["task_id"]
    await asyncio.sleep(17)
    # Get results
    result = requests.get(f"http://localhost:11235/task/{task_id}", headers=headers)
    print(result.json())
    return result


async def test_news_crawl(url: str):
    async with AsyncWebCrawler(
        verbose=True,
        headless=False,
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
        # print(result.markdown_v2)
        return result.markdown_v2


def post_request(target_url: str):
    url = "http://localhost:8000/crawl"
    data = {
        "url": target_url
    }
    response = requests.post(url, json=data)
    print(response.json())


if __name__ == "__main__":
    url = "https://www.rightmove.co.uk/properties/134329280#/?channel=RES_NEW"
    # url = "https://www.zoopla.co.uk/for-sale/details/69117958/?search_identifier=789715c86a8096916567c9304f6855f82e6d66b34a9be63fd28d14a80b5b81a9&weekly_featured=1&utm_content=featured_listing"
    post_request(url)
    # asyncio.run(test_news_crawl(url))
