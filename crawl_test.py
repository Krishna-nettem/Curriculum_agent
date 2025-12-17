# crawl_test.py
import asyncio
from crawl4ai import AsyncWebCrawler

async def test():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url="https://en.wikipedia.org/wiki/Generative_artificial_intelligence",
        )

        print("=== TEXT ===")
        print(result.markdown[:1000])

        print("\n=== IMAGES ===")
        for img in result.media.get("images", [])[:5]:
            print(img)

asyncio.run(test())
