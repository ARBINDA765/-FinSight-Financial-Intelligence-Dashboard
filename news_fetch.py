"""
Financial News Fetcher
Fetches latest financial news from multiple sources and saves to CSV
"""

import pandas as pd
import requests
from datetime import datetime, timedelta
import json
import os
from typing import List, Dict
import time

# Configuration
CSV_FILE = 'finance_news.csv'
MAX_ARTICLES = 100

def fetch_from_newsapi(api_key: str = None) -> List[Dict]:
    """
    Fetch financial news from NewsAPI
    Get your free API key from: https://newsapi.org/
    """
    if not api_key:
        api_key = os.environ.get('NEWS_API_KEY', '')
    
    if not api_key:
        print("⚠️ NewsAPI key not found. Skipping NewsAPI...")
        return []
    
    try:
        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': 'finance OR stock market OR economy OR trading',
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 50,
            'apiKey': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        articles = []
        
        for article in data.get('articles', []):
            articles.append({
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'url': article.get('url', ''),
                'source': article.get('source', {}).get('name', 'Unknown'),
                'date': article.get('publishedAt', ''),
                'category': 'Finance',
                'image_url': article.get('urlToImage', '')
            })
        
        print(f"✅ Fetched {len(articles)} articles from NewsAPI")
        return articles
    
    except Exception as e:
        print(f"❌ Error fetching from NewsAPI: {str(e)}")
        return []

def fetch_from_rss_feeds() -> List[Dict]:
    """
    Fetch financial news from RSS feeds (no API key required)
    """
    try:
        import feedparser
    except ImportError:
        print("⚠️ feedparser not installed. Run: pip install feedparser")
        return []
    
    feeds = [
        ('https://feeds.finance.yahoo.com/rss/2.0/headline', 'Yahoo Finance', 'Market News'),
        ('https://www.cnbc.com/id/100003114/device/rss/rss.html', 'CNBC', 'Finance'),
        ('https://www.ft.com/?format=rss', 'Financial Times', 'Business'),
    ]
    
    articles = []
    
    for feed_url, source, category in feeds:
        try:
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:20]:  # Limit to 20 per feed
                articles.append({
                    'title': entry.get('title', ''),
                    'description': entry.get('summary', entry.get('description', '')),
                    'url': entry.get('link', ''),
                    'source': source,
                    'date': entry.get('published', ''),
                    'category': category,
                    'image_url': ''
                })
            
            print(f"✅ Fetched {min(20, len(feed.entries))} articles from {source}")
            time.sleep(1)  # Be nice to servers
            
        except Exception as e:
            print(f"❌ Error fetching from {source}: {str(e)}")
            continue
    
    return articles

def fetch_from_google_news() -> List[Dict]:
    """
    Fetch financial news from Google News RSS (no API key required)
    """
    try:
        import feedparser
    except ImportError:
        return []
    
    try:
        # Google News RSS for business/finance
        feed_url = 'https://news.google.com/rss/search?q=finance+OR+stocks+OR+market&hl=en-US&gl=US&ceid=US:en'
        feed = feedparser.parse(feed_url)
        
        articles = []
        for entry in feed.entries[:30]:
            articles.append({
                'title': entry.get('title', ''),
                'description': entry.get('summary', ''),
                'url': entry.get('link', ''),
                'source': 'Google News',
                'date': entry.get('published', ''),
                'category': 'Finance',
                'image_url': ''
            })
        
        print(f"✅ Fetched {len(articles)} articles from Google News")
        return articles
    
    except Exception as e:
        print(f"❌ Error fetching from Google News: {str(e)}")
        return []

def fetch_from_alphavantage(api_key: str = None) -> List[Dict]:
    """
    Fetch financial news from Alpha Vantage
    Get your free API key from: https://www.alphavantage.co/support/#api-key
    """
    if not api_key:
        api_key = os.environ.get('ALPHA_VANTAGE_KEY', '')
    
    if not api_key:
        print("⚠️ Alpha Vantage key not found. Skipping Alpha Vantage...")
        return []
    
    try:
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'NEWS_SENTIMENT',
            'topics': 'finance,economy',
            'apikey': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        articles = []
        
        for article in data.get('feed', [])[:30]:
            articles.append({
                'title': article.get('title', ''),
                'description': article.get('summary', ''),
                'url': article.get('url', ''),
                'source': article.get('source', 'Unknown'),
                'date': article.get('time_published', ''),
                'category': 'Finance',
                'image_url': article.get('banner_image', '')
            })
        
        print(f"✅ Fetched {len(articles)} articles from Alpha Vantage")
        return articles
    
    except Exception as e:
        print(f"❌ Error fetching from Alpha Vantage: {str(e)}")
        return []

def clean_and_deduplicate(articles: List[Dict]) -> pd.DataFrame:
    """
    Clean, standardize, and deduplicate articles
    """
    if not articles:
        print("⚠️ No articles to process")
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(articles)
    
    # Remove duplicates based on title
    df = df.drop_duplicates(subset=['title'], keep='first')
    
    # Clean and standardize dates
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Remove articles with missing critical data
    df = df.dropna(subset=['title', 'url'])
    
    # Fill missing descriptions
    df['description'] = df['description'].fillna('')
    
    # Sort by date (newest first)
    df = df.sort_values('date', ascending=False)
    
    # Limit to max articles
    df = df.head(MAX_ARTICLES)
    
    print(f"✅ Cleaned dataset: {len(df)} unique articles")
    return df

def save_to_csv(df: pd.DataFrame, filename: str = CSV_FILE):
    """
    Save articles to CSV file
    """
    try:
        df.to_csv(filename, index=False)
        print(f"✅ Saved {len(df)} articles to {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving to CSV: {str(e)}")
        return False

def main():
    """
    Main function to fetch and save financial news
    """
    print("=" * 60)
    print("🚀 Starting Financial News Fetch")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    all_articles = []
    
    # Fetch from multiple sources
    print("\n📡 Fetching from RSS feeds (no API key needed)...")
    all_articles.extend(fetch_from_rss_feeds())
    
    print("\n📡 Fetching from Google News...")
    all_articles.extend(fetch_from_google_news())
    
    # Uncomment and add API keys to fetch from these sources:
    
    # print("\n📡 Fetching from NewsAPI...")
    # all_articles.extend(fetch_from_newsapi())
    
    # print("\n📡 Fetching from Alpha Vantage...")
    # all_articles.extend(fetch_from_alphavantage())
    
    # Clean and save
    print("\n🧹 Cleaning and deduplicating...")
    df = clean_and_deduplicate(all_articles)
    
    if not df.empty:
        print("\n💾 Saving to CSV...")
        success = save_to_csv(df)
        
        if success:
            print("\n" + "=" * 60)
            print("✅ SUCCESS: News fetch completed!")
            print(f"📊 Total articles: {len(df)}")
            print(f"📁 File: {CSV_FILE}")
            print("=" * 60)
        else:
            print("\n❌ Failed to save data")
            exit(1)
    else:
        print("\n❌ No articles fetched. Check your API keys or network connection.")
        
        # Create empty CSV with headers to prevent app errors
        empty_df = pd.DataFrame(columns=['title', 'description', 'url', 'source', 'date', 'category', 'image_url'])
        save_to_csv(empty_df)
        exit(1)

if __name__ == "__main__":
    main()
