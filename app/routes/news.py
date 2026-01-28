from fastapi import APIRouter, Query
from app.utils.storage import load_news

router = APIRouter()

@router.get("/latest")
def latest_news():
    return load_news()

@router.get("/category")
def by_category(category: str):
    news = load_news()
    return [n for n in news if n["category"].lower() == category.lower()]

@router.get("/search")
def search_news(q: str = Query(..., min_length=2)):
    news = load_news()
    return [
        n for n in news
        if q.lower() in n["title"].lower()
        or q.lower() in n["content"].lower()
    ]