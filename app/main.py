import utils.clients
import utils.http_session
import utils.transport
import utils.session
from fastapi import FastAPI
from app.routes import news

app = FastAPI(
    title="Sri Lankan News API",
    description="MVP REST API for Sri Lankan news scraping",
    version="1.0"
)

app.include_router(news.router, prefix="/news")