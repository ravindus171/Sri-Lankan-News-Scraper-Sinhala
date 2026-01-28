from app.scrapers.hiru import scrape_hiru_latest
from app.scrapers.adaderana import scrape_adaderana_latest
from app.utils.storage import save_news

if __name__ == "__main__":
    print("Scraping Hiru News...")
    hiru_news = scrape_hiru_latest()
    
    print("Scraping Ada Derana...")
    derana_news = scrape_adaderana_latest()
    
    all_news = hiru_news + derana_news
    save_news(all_news)
    print(f"Saved {len(all_news)} articles total ({len(hiru_news)} Hiru, {len(derana_news)} Derana)")