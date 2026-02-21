"""Reuters RSS crawler."""
from typing import List

from app.config import RSS_FEEDS_BY_CATEGORY
from app.models import Article
from .base_rss import fetch_feed

CATEGORY = "Reuters World"


def crawl_reuters() -> List[Article]:
    """Crawl Reuters World feed."""
    articles: List[Article] = []
    for url in RSS_FEEDS_BY_CATEGORY.get(CATEGORY, []):
        articles.extend(fetch_feed(url, CATEGORY))
    return articles
