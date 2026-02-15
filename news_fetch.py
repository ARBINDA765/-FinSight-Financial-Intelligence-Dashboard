
import feedparser
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import quote_plus
import os
import time
import email.utils as email_utils
import re
from pathlib import Path

topics = [
    "Mutual Fund India",
    "ETF",
    "IPO",
    "NPS",
    "Income Tax",
    "MOU Sign",
    "Stock market",
    "Gold ",
    "Silver ",
    "Commodity ",
    # Exchange / indices / stock-specific topics
    "NSE",
    "BSE ",
    "Nifty 50 ",
    "Nifty 100 ",
    "Nifty ",
    "Stock price ",
    "Intraday stock ",
    "Pharma ",
    "Pharmaceutical stocks",
    "Odisha Investment ",
    "MOU Deal"
]

all_news = []

for topic in topics:
    q = quote_plus(topic)
    url = f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        feed = feedparser.parse(url)
    except Exception:
        continue

    for entry in feed.entries:
        # Determine published datetime (prefer structured time)
        published_dt = None
        if entry.get('published_parsed'):
            published_dt = datetime(*entry.published_parsed[:6])
        else:
            pub = entry.get('published', '')
            if pub:
                try:
                    published_dt = email_utils.parsedate_to_datetime(pub)
                except Exception:
                    published_dt = None

        if not published_dt:
            # skip entries without a parsable published date
            continue

        # normalize timezone-aware datetimes to naive UTC for comparison
        if published_dt.tzinfo is not None:
            published_dt = published_dt.astimezone(datetime.utcfromtimestamp(0).tzinfo or None)

        # Only include items from the last 3 days
        if datetime.utcnow() - published_dt > timedelta(days=3):
            continue

        source_title = entry.get('source', {}).get('title', 'Unknown')
        published = entry.get('published', '')
        # Build a short overview/context for the article from feed summary/description
        overview_raw = entry.get('summary') or entry.get('description') or ''
        overview = re.sub(r'<[^>]+>', '', overview_raw).strip()
        all_news.append({
            "title": entry.get('title', ''),
            "source": source_title,
            "published": published,
            "overview": overview,
            "link": entry.get('link', ''),
            "topic": topic,
            "date_loaded": datetime.now().strftime("%Y-%m-%d")
        })

df = pd.DataFrame(all_news)

# Ensure data directory exists (relative to repo root: parent of scripts)
script_dir = Path(__file__).resolve().parent
data_dir = script_dir.parent / "data"
data_dir.mkdir(parents=True, exist_ok=True)
output_file = data_dir / "finance_news.csv"

df.to_csv(output_file, index=False)
print(f"FinSight data refreshed -> {output_file}")
