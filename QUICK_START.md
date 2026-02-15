# 🚀 Quick Start Guide

Test your FinSight dashboard locally before deploying to Streamlit Cloud.

## Local Testing (3 Simple Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Fetch Initial News Data
```bash
python news_fetch.py
```
This creates `finance_news.csv` with the latest financial news.

### 3. Run Dashboard Locally
```bash
streamlit run app.py
```
Opens at http://localhost:8501

---

## Test the Auto-Update Workflow Locally

### Manual Trigger
```bash
# Fetch fresh news
python news_fetch.py

# Restart Streamlit (Ctrl+C then re-run)
streamlit run app.py
```

### Scheduled Updates (Optional - For Local Testing)
Create a cron job or scheduled task to run `news_fetch.py` every 4 hours:

**Linux/Mac:**
```bash
# Open crontab
crontab -e

# Add this line (runs every 4 hours)
0 */4 * * * cd /path/to/your/project && python news_fetch.py
```

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily, repeat every 4 hours
4. Action: Run `python news_fetch.py`

---

## Verify Everything Works

### ✅ Checklist
- [ ] `requirements.txt` installs successfully
- [ ] `news_fetch.py` runs without errors
- [ ] `finance_news.csv` is created with data
- [ ] `streamlit run app.py` opens dashboard
- [ ] Dashboard displays news articles
- [ ] No errors in terminal

### 🐛 Common Issues

**Problem:** `ModuleNotFoundError`
```bash
# Solution: Install missing package
pip install package-name
```

**Problem:** `finance_news.csv` is empty
```bash
# Solution: Check news_fetch.py output for errors
# May need API keys for some sources
```

**Problem:** Dashboard shows "No data"
```bash
# Solution: Verify CSV exists and has data
ls -lh finance_news.csv
head finance_news.csv
```

---

## Next Steps

Once local testing works:
1. Follow `DEPLOYMENT_GUIDE.md` for Streamlit Cloud deployment
2. Enable GitHub Actions for auto-updates
3. Enjoy your automated financial dashboard! 🎉

---

## Adding API Keys (Optional)

Some news sources require API keys for more articles:

### NewsAPI (Free Tier: 100 requests/day)
1. Get key: https://newsapi.org/
2. Add to `news_fetch.py` line 196 (uncomment)
3. Or set environment variable:
   ```bash
   export NEWS_API_KEY="your_key_here"
   ```

### Alpha Vantage (Free Tier: 25 requests/day)
1. Get key: https://www.alphavantage.co/support/#api-key
2. Add to `news_fetch.py` line 199 (uncomment)
3. Or set environment variable:
   ```bash
   export ALPHA_VANTAGE_KEY="your_key_here"
   ```

For Streamlit Cloud deployment, add these in app settings → Secrets.

---

**Need help?** Check `DEPLOYMENT_GUIDE.md` for detailed troubleshooting.
