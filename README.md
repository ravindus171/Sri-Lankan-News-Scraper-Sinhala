# Sri Lankan News Scraper API

A lightweight FastAPI-based web scraper and REST API that aggregates latest news from major Sri Lankan news portals (Hiru News and Ada Derana) in Sinhala.

## 🚀 Features

* **Multi-Source Scraping**: Aggregates news from Hiru News (Sinhala) and Ada Derana (Sinhala).
* **Automated Extraction**: Extracts titles, full content, categories, and feature images.
* **REST API**: Serves scraped news via structured endpoints.
* **Search & Filter**: Built-in support for searching through news and filtering by category.
* **JSON Storage**: Simple file-based storage for easy portability.

## 📁 Project Structure

```text
NewsScrape/
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── routes/
│   │   └── news.py      # API endpoint definitions
│   ├── scrapers/
│   │   ├── hiru.py      # Hiru News Sinhala scraper
│   │   └── adaderana.py # Ada Derana Sinhala scraper
│   └── utils/
│       └── storage.py   # JSON file handling logic
├── data/
│   └── news.json       # Stored news data (Auto-generated)
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── run_scraper.py      # Script to manually trigger scraping
```

## 🛠️ Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd NewsScrape
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📈 Usage

### 1. Run the Scraper
To fetch the latest news and update the local database:
```bash
python run_scraper.py
```
This will fetch the 10 latest articles from both Hiru and Ada Derana and save them to `data/news.json`.

### 2. Start the API Server
To start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## 🔌 API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/news/latest` | `GET` | Returns all scraped news articles. |
| `/news/category?category=<name>` | `GET` | Filters news by category (e.g., General). |
| `/news/search?q=<query>` | `GET` | Searches for news by keyword in title or content. |
| `/docs` | `GET` | Interactive Swagger UI documentation. |

## 🧪 Tech Stack

* **Framework**: FastAPI (Python)
* **Scraping**: BeautifulSoup4, Requests
* **Storage**: JSON (File-based)
* **Server**: Uvicorn

