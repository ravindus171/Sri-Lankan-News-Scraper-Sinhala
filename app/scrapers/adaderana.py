import requests
import time
from bs4 import BeautifulSoup

BASE_URL = "https://sinhala.adaderana.lk/"
HOT_NEWS_URL = "https://sinhala.adaderana.lk/sinhala-hot-news.php"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_adaderana_latest():
    articles = []
    try:
        res = requests.get(HOT_NEWS_URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Find news links - typically they are relative links starting with "news/"
        # We target the main news container if possible, but identifying by href pattern is usually safe enough here
        links = soup.select("a[href*='news/']")

        urls = []
        for link in links:
            href = link.get("href")
            if not href:
                continue
            
            # Clean href
            href = href.strip()
            
            # Ignore comment anchors
            if "#" in href:
                href = href.split("#")[0]

            # Construct full URL
            if not href.startswith("http"):
                full_url = BASE_URL + href.lstrip("/")
            else:
                full_url = href

            # Filter valid news URLs (ensure it's from adaderana)
            if "adaderana.lk" in full_url and "/news/" in full_url:
                 urls.append(full_url)

        # Deduplicate and take top 10
        urls = list(dict.fromkeys(urls))[:10]

        for url in urls:
            try:
                article_res = requests.get(url, headers=HEADERS, timeout=10)
                article_soup = BeautifulSoup(article_res.text, "html.parser")

                title_tag = article_soup.select_one("h1")
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)

                # Content extraction
                content_div = article_soup.select_one(".news-content")
                if content_div:
                    # Remove ads or scripts if necessary
                    for script in content_div(["script", "style"]):
                        script.decompose()
                    content = content_div.get_text(separator="\n", strip=True)
                else:
                    # Fallback
                    paras = article_soup.select("p")
                    content = "\n".join(p.get_text(strip=True) for p in paras)

                # Image extraction
                image_url = None
                # Banner image
                banner_img = article_soup.select_one(".news-banner img")
                if banner_img:
                    image_url = banner_img.get("src")
                
                # Fallback to standard image match
                if not image_url:
                    img_tag = article_soup.select_one(".news-content img")
                    if img_tag:
                         image_url = img_tag.get("src")
                
                # Validation for relative image URLs
                if image_url and not image_url.startswith("http"):
                    image_url = BASE_URL + image_url.lstrip("/")

                articles.append({
                    "source": "Ada Derana (Sinhala)",
                    "title": title,
                    "category": "General",
                    "content": content,
                    "image_url": image_url,
                    "url": url
                })

                time.sleep(1)

            except Exception as e:
                print(f"Error scraping Ada Derana article {url}: {e}")

    except Exception as e:
        print("Error fetching Ada Derana main page:", e)

    return articles
