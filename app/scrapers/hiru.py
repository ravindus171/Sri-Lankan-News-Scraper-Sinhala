import requests
import time
from bs4 import BeautifulSoup

# Base URL for Sinhala news
HIRU_URL = "https://hirunews.lk/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_hiru_latest():
    articles = []
    try:
        res = requests.get(HIRU_URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Select all links, we will filter manually
        links = soup.select("a[href]")

        urls = []
        for link in links:
            href = link.get("href")
            if not href:
                continue
            href = href.strip()

            # Handle relative URLs
            if href.startswith("/"):
                href = "https://hirunews.lk" + href
            
            # Must be a hirunews link
            if "hirunews.lk" not in href:
                continue

            # Exclude English, Tamil, and other sections
            if "/en/" in href or "/english/" in href or "/tm/" in href or "/tamil/" in href:
                continue
            
            # Valid articles usually have a number in the URL (ID)
            if not any(char.isdigit() for char in href):
                continue

            urls.append(href)

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

                # Target specific content container
                content_div = article_soup.select_one("#this-article")
                if not content_div:
                    content_div = article_soup.select_one(".article-content")
                
                if content_div:
                    # Use get_text with separator to handle text nodes directly (common in Sinhala/Hiru)
                    content = content_div.get_text(separator="\n", strip=True)
                else:
                    # Fallback to paragraphs if no main container found
                    paras = article_soup.select("p") 
                    content = "\n".join(p.get_text(strip=True) for p in paras if p.get_text(strip=True))

                # Extract image
                image_url = None
                og_image = article_soup.select_one("meta[property='og:image']")
                if og_image:
                    image_url = og_image.get("content")
                
                if not image_url:
                    img_tag = article_soup.select_one(".featured-image img")
                    if img_tag:
                         image_url = img_tag.get("src")

                articles.append({
                    "source": "Hiru News (Sinhala)",
                    "title": title,
                    "category": "General",
                    "content": content,
                    "image_url": image_url,
                    "url": url
                })

                time.sleep(1)

            except Exception as e:
                print(f"Error scraping article {url}: {e}")

    except Exception as e:
        print("Error fetching main page:", e)

    return articles