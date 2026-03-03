"""FastAPI web server for news frontend."""
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api import router as api_router
from app.limiter import limiter

app = FastAPI(
    title="News AI System",
    description="AI-powered news aggregator with Vietnamese translation",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security headers (run for every response)
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Google Search Console verification (must be at root; register early)
GOOGLE_VERIFICATION_CONTENT = "google-site-verification: googlea64e30f7786323f3.html"


@app.get("/googlea64e30f7786323f3.html", response_class=HTMLResponse, include_in_schema=False)
async def google_verification():
    """Serve Google Search Console verification at root (required by Google)."""
    path = STATIC_DIR / "googlea64e30f7786323f3.html"
    if path.exists():
        return HTMLResponse(content=path.read_text(encoding="utf-8"))
    return HTMLResponse(content=GOOGLE_VERIFICATION_CONTENT)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main frontend page."""
    html_file = STATIC_DIR / "index.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Frontend not found</h1>")


@app.get("/article", response_class=HTMLResponse)
async def article_page(request: Request):
    """Serve the article detail page (no id; client may redirect to canonical /article/{id})."""
    html_file = STATIC_DIR / "article.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Article page not found</h1>")


@app.get("/article/{article_id}", response_class=HTMLResponse)
async def article_by_id(request: Request, article_id: str):
    """Serve the article detail page for /article/{id} (same HTML; JS loads article by id)."""
    html_file = STATIC_DIR / "article.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Article page not found</h1>")


@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """Serve the About page (SEO 3.3 – Nội dung bổ sung)."""
    html_file = STATIC_DIR / "about.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>About page not found</h1>")


@app.get("/guide", response_class=HTMLResponse)
async def guide_page(request: Request):
    """Serve the Guide page (SEO 3.3 – Nội dung bổ sung)."""
    html_file = STATIC_DIR / "guide.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Guide page not found</h1>")


@app.get("/faq", response_class=HTMLResponse)
async def faq_page(request: Request):
    """Serve the FAQ page (SEO 3.3 – Nội dung bổ sung)."""
    html_file = STATIC_DIR / "faq.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>FAQ page not found</h1>")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Redirect browser favicon request to the PNG in static."""
    return RedirectResponse(url="/static/img/favicon.png", status_code=302)


@app.get("/health")
@limiter.exempt
async def health_check(request: Request):
    """Health check endpoint (exempt from rate limit)."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.web_server:app", host="0.0.0.0", port=8000, reload=True)
