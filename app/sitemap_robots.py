"""
Sitemap & robots endpoints (SEO Phase 2.3).
Register with: app.include_router(sitemap_robots_router)
"""
from fastapi import APIRouter, Request
from fastapi.responses import Response

from app.seo import (
    build_sitemap_xml,
    build_robots_txt,
    _all_category_names,
)

sitemap_robots_router = APIRouter()


def _get_articles_for_sitemap():
    """Get list of articles for sitemap (id + published). Optional MongoDB."""
    try:
        from app.database.mongo import get_articles_collection
        col = get_articles_collection()
        cursor = col.find(
            {"isShow": True},
            {"_id": 1, "published": 1}
        ).sort("published", -1)
        return list(cursor)
    except Exception:
        return []


@sitemap_robots_router.get("/sitemap.xml", include_in_schema=False)
async def sitemap_xml(request: Request):
    """Dynamic sitemap: home, category pages, all articles from DB."""
    base_url = str(request.base_url).rstrip("/")
    articles = _get_articles_for_sitemap()
    categories = _all_category_names()
    xml = build_sitemap_xml(base_url, articles, categories)
    return Response(
        content=xml,
        media_type="application/xml",
        headers={"Cache-Control": "public, max-age=3600"},
    )


@sitemap_robots_router.get("/robots.txt", include_in_schema=False)
async def robots_txt(request: Request):
    """robots.txt: allow /, disallow /api/ and /health, point to Sitemap."""
    base_url = str(request.base_url).rstrip("/")
    content = build_robots_txt(base_url)
    return Response(
        content=content,
        media_type="text/plain",
        headers={"Cache-Control": "public, max-age=86400"},
    )
