"""BBC RSS crawler: Tin thế giới, Kinh tế, Công nghệ."""
from typing import List

from app.config import RSS_FEEDS_BY_CATEGORY
from app.models import Article
from .base_rss import fetch_feed

BBC_CATEGORIES = ["Tin thế giới", "Kinh tế", "Công nghệ"]


def crawl_bbc() -> List[Article]:
    """Crawl all BBC feeds and return combined articles."""
    articles: List[Article] = []
    for category in BBC_CATEGORIES:
        urls = RSS_FEEDS_BY_CATEGORY.get(category, [])
        for url in urls:
            if "bbci.co.uk" in url or "bbc." in url:
                articles.extend(fetch_feed(url, category))
    return articles
