import os
import asyncio
from typing import List, Tuple
from tavily import TavilyClient
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from logger import get_logger
from llm import call_gemini, call_ollama
from prompts import CURRICULUM_PROMPT


logger = get_logger()


def tavily_search(query: str, max_results: int = 5) -> List[str]:
    
    try:
        logger.info(f"Searching with Tavily for query: {query}")
        tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
        response = tavily_client.search(
            query=f"{query} tutorial guide comprehensive",
            search_depth="advanced",  
            max_results=max_results,
            include_domains=[],
            exclude_domains=[
                'quora.com', 'stackoverflow.com',
                'zhihu.com', 'baidu.com', 'csdn.net', 'udemy.com', 
                'coursera.org', 'linkedin.com', 'facebook.com', 'twitter.com', 'magai.co'
            ]
        )
        
        urls = [result.get('url', '') for result in response.get('results', []) if result.get('url')]
        
        logger.info(f"Tavily returned {len(urls)} URLs for crawling")
        return urls[:max_results]
    
    except Exception:
        logger.exception("Tavily search failed")
        return []


async def _crawl_single(crawler: AsyncWebCrawler, url: str) -> Tuple[str, list]:
    
    try:
        logger.info(f"Crawling URL: {url}")
        
        
        config = CrawlerRunConfig(
            
            excluded_tags=['nav', 'footer', 'header', 'aside', 'form', 'button', 
                          'script', 'style', 'iframe', 'advertisement', 'sidebar'],
            
            
            exclude_external_links=True,
            exclude_social_media_links=True,
            exclude_external_images=False,  
            
            
            word_count_threshold=20,  
            
            
            cache_mode=CacheMode.BYPASS,
            
            
            css_selector="article, main, .content, .post, .article, [role='main']",
        )
        
        res = await crawler.arun(url=url, config=config)
        
        
        text = res.markdown.raw_markdown if res.markdown else ""
        
        
        images = [
            img.get("src") for img in (res.media.get("images") or []) 
            if img.get("src") and not any(x in img.get("src", "") for x in ['logo', 'icon', 'avatar', 'thumbnail'])
        ]
        
        
        lines = text.split('\n')
        cleaned_lines = []
        seen_lines = set()
        
        for line in lines:
            line = line.strip()
            
            if len(line) < 10 or line in seen_lines:
                continue
            
            if any(x in line.lower() for x in ['cookie', 'subscribe', 'newsletter', 'menu', 'sign in', 'log in']):
                continue
            cleaned_lines.append(line)
            seen_lines.add(line)
        
        cleaned_text = '\n'.join(cleaned_lines)
        
        
        return cleaned_text[:15000], images[:10]
        
    except Exception:
        logger.exception(f"Crawl failed for url: {url}")
        return "", []


async def crawl_urls_full(urls: List[str], max_pages: int = 5):
    
    notes = []
    all_images = []
    
    async with AsyncWebCrawler(verbose=False) as crawler:
        for url in urls[:max_pages]:
            text, images = await _crawl_single(crawler, url)
            
            if text and len(text) > 500:  
                notes.append({
                    "url": url,
                    "text": text
                })
                logger.info(f"Extracted {len(text)} chars and {len(images)} images from {url}")
            else:
                logger.warning(f"Skipped {url} - insufficient content")
            
            all_images.extend(images)
    
    return notes, all_images


def research_agent(topic: str):
    logger.info(f"Starting research_agent for topic: {topic}")
    query = f"{topic} comprehensive guide"
    
    urls = tavily_search(query, max_results=10)
    
    if not urls:
        logger.warning("No URLs found by Tavily search")
        return {"summary": "no_results", "notes": [], "images": [], "sources": []}
    
    try:
        notes, images = asyncio.run(crawl_urls_full(urls, max_pages=6))
        
        if not notes:
            logger.warning("Crawling returned no content")
            return {"summary": "no_content", "notes": [], "images": [], "sources": []}
        
        sources = [n["url"] for n in notes]
        total_chars = sum(len(n["text"]) for n in notes)
        logger.info(f"Research completed: {len(notes)} articles crawled ({total_chars} chars), {len(images)} images extracted")
        
        return {
            "summary": f"Crawled {len(notes)} high-quality articles",
            "notes": notes,
            "images": images,
            "sources": sources
        }
    except Exception:
        logger.exception("research_agent failed during crawling")
        return {"summary": "error", "notes": [], "images": [], "sources": []}


def curriculum_agent(topic: str,research_data: dict):
    logger.info(f"Starting curriculum_agent for topic: {topic}")
    
    notes_texts = [n["text"] for n in research_data.get("notes", [])][:6]
    images = research_data.get("images", [])[:8]
    sources = research_data.get("sources", [])[:6]

    research_blob = "\n\n---\n\n".join(notes_texts)  
    images_blob = "\n".join(images) or "No images available"
    
    logger.info(f"Curriculum generation with {len(research_blob)} chars of research content from {len(sources)} sources")
    
    prompt = CURRICULUM_PROMPT.format(
        topic=topic,
        research=research_blob,
        images=images_blob
    )

    
    try:
        logger.info("Trying Gemini for curriculum generation")
        md = call_gemini(prompt)
        logger.info("Curriculum generated by Gemini")
        return {"text": md, "source": "gemini", "sources": sources}
    except Exception:
        logger.warning("Gemini failed; attempting Ollama fallback")

    #calling only the topic beacause prompt is too large and it takes a lot of time for ollama (when I tried) to generate (basic cpu :(  )
    try:
        md = call_ollama(topic)
        logger.info("Curriculum generated by Ollama")
        return {"text": md, "source": "ollama", "sources": "none"}
    except Exception:
        logger.exception("Both LLM calls failed in curriculum_agent")
        
        #just for fun hehe
        return {"text": "Ask ChatGpt", "source": "none", "sources": "none"}
