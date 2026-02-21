"""Crypto RSS crawler: CoinDesk, Cointelegraph."""
from datetime import datetime
from typing import List

from app.config import RSS_FEEDS_BY_CATEGORY, CRAWL_LIMIT_PER_FEED
from app.models import Article
from .base_rss import fetch_feed

CATEGORY = "Crypto"


def _sort_key(a: Article) -> datetime:
    """Dùng để sắp xếp: tin mới nhất trước; không có published thì xếp cuối."""
    return a.published or datetime.min


def crawl_crypto() -> List[Article]:
    """Crawl CoinDesk và Cointelegraph; gộp lại, lấy đúng top N tin mới nhất cho cả category."""
    articles: List[Article] = []
    for url in RSS_FEEDS_BY_CATEGORY.get(CATEGORY, []):
        # Lấy nhiều hơn mỗi feed để sau khi gộp còn đủ để sort và chọn top N
        articles.extend(fetch_feed(url, CATEGORY))
    articles.sort(key=_sort_key, reverse=True)
    return articles[:CRAWL_LIMIT_PER_FEED]
