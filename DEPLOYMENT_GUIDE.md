# FinSight - Deployment Guide

Complete guide to deploy your FinSight Financial Intelligence Dashboard on Streamlit Cloud with automated news updates every 4 hours.

---

## 📋 Overview

This deployment setup includes:
- ✅ Streamlit Cloud hosting for the dashboard
- ✅ Automated news fetching every 4 hours via GitHub Actions
- ✅ Automatic CSV updates pushed to GitHub
- ✅ Live dashboard at: https://finsight-financial-intelligence-dashboard.streamlit.app/

---

## 🚀 Step-by-Step Deployment

### Step 1: Update Your GitHub Repository

1. **Upload these new files to your repository:**
   - `.github/workflows/update_news.yml` → Enables automated news fetching
   - `.streamlit/config.toml` → Streamlit configuration

2. **Commit and push to GitHub:**
   ```bash
   git add .github/workflows/update_news.yml
   git add .streamlit/config.toml
   git commit -m "Add deployment configuration files"
   git push origin main
   ```

### Step 2: Enable GitHub Actions

1. Go to your repository: https://github.com/ARBINDA765/-FinSight-Financial-Intelligence-Dashboard
2. Click on **"Settings"** tab
3. Go to **"Actions"** → **"General"** (left sidebar)
4. Under **"Workflow permissions"**, select:
   - ✅ **"Read and write permissions"**
   - ✅ **"Allow GitHub Actions to create and approve pull requests"**
5. Click **"Save"**

### Step 3: Test GitHub Actions (Optional but Recommended)

1. Go to **"Actions"** tab in your repository
2. Click on **"Update Financial News Data"** workflow
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait 1-2 minutes and check if `finance_news.csv` was updated
5. If successful, you'll see a new commit: "Auto-update: Financial news data"

### Step 4: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud:** https://streamlit.io/cloud
2. **Sign in with GitHub**
3. Click **"New app"**
4. Configure deployment:
   - **Repository:** `ARBINDA765/-FinSight-Financial-Intelligence-Dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL (Custom subdomain):** `finsight-financial-intelligence-dashboard`

5. Click **"Advanced settings"** (optional):
   - **Python version:** `3.11`
   - Add any API keys if your `news_fetch.py` requires them

6. Click **"Deploy!"**

### Step 5: Verify Deployment

1. **Wait 3-5 minutes** for Streamlit to build and deploy
2. Your dashboard will be live at: 
   ```
   https://finsight-financial-intelligence-dashboard.streamlit.app/
   ```
3. Verify the dashboard loads correctly with data from `finance_news.csv`

---

## ⚙️ How It Works

### Automated News Updates

The GitHub Actions workflow (`update_news.yml`) automatically:
1. **Runs every 4 hours** (00:00, 04:00, 08:00, 12:00, 16:00, 20:00 UTC)
2. **Executes** `news_fetch.py` to fetch latest financial news
3. **Updates** `finance_news.csv` with new data
4. **Commits and pushes** changes back to GitHub
5. **Triggers** Streamlit Cloud to reload the dashboard

### Streamlit Cloud Behavior

- **Auto-reloads** when `finance_news.csv` is updated on GitHub
- **Always displays** the latest news data
- **No manual intervention** required

---

## 🛠️ Troubleshooting

### GitHub Actions Not Running

**Problem:** Workflow doesn't run automatically

**Solution:**
- Check "Settings" → "Actions" → "General" → Ensure "Read and write permissions" is enabled
- Go to "Actions" tab → "Update Financial News Data" → "Enable workflow" if disabled
- Manually trigger once: "Actions" → "Run workflow"

### Streamlit App Not Updating

**Problem:** Dashboard shows old data after GitHub Actions runs

**Solution:**
- Streamlit Cloud usually auto-updates within 1-2 minutes
- Force reload: Go to Streamlit Cloud dashboard → Click "Reboot app"
- Check `finance_news.csv` on GitHub to verify data was updated

### API Rate Limits

**Problem:** `news_fetch.py` fails due to API limits

**Solution:**
- Add API keys to Streamlit Cloud: App settings → Secrets
- Format in `.streamlit/secrets.toml` style:
  ```toml
  NEWS_API_KEY = "your_api_key_here"
  ```
- Update `news_fetch.py` to read from Streamlit secrets

### CSV Not Updating

**Problem:** `finance_news.csv` not being committed

**Solution:**
- Check GitHub Actions logs: "Actions" tab → Click on latest run → View logs
- Verify `news_fetch.py` successfully creates/updates CSV
- Ensure CSV is not in `.gitignore`

---

## 📊 Monitoring

### Check GitHub Actions

1. Go to **"Actions"** tab
2. View recent runs of **"Update Financial News Data"**
3. Green checkmark ✅ = Success
4. Red X ❌ = Failed (click to see logs)

### Check Streamlit Logs

1. Go to Streamlit Cloud dashboard
2. Click on your app
3. View logs for errors
4. Check "Last deployed" timestamp

---

## 🔧 Customization

### Change Update Frequency

Edit `.github/workflows/update_news.yml`:

```yaml
# Every 2 hours
- cron: '0 */2 * * *'

# Every 6 hours
- cron: '0 */6 * * *'

# Daily at 9 AM UTC
- cron: '0 9 * * *'

# Every hour
- cron: '0 * * * *'
```

Use [crontab.guru](https://crontab.guru/) to generate custom schedules.

### Add Environment Variables

If `news_fetch.py` needs API keys:

1. **For GitHub Actions:**
   - Go to "Settings" → "Secrets and variables" → "Actions"
   - Click "New repository secret"
   - Add: `NEWS_API_KEY` with your key

2. **Update workflow file:**
   ```yaml
   - name: Fetch latest financial news
     env:
       NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}
     run: |
       python news_fetch.py
   ```

3. **For Streamlit Cloud:**
   - Go to app settings
   - Add to "Secrets" section:
     ```toml
     NEWS_API_KEY = "your_key_here"
     ```

---

## 📝 Files Structure

After deployment, your repository should look like:

```
-FinSight-Financial-Intelligence-Dashboard/
├── .github/
│   └── workflows/
│       └── update_news.yml          # ← Auto-update workflow
├── .streamlit/
│   └── config.toml                  # ← Streamlit configuration
├── app.py                           # Main dashboard file
├── news_fetch.py                    # News fetching script
├── finance_news.csv                 # News data (auto-updated)
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

---

## ✅ Deployment Checklist

- [ ] Upload `.github/workflows/update_news.yml` to repository
- [ ] Upload `.streamlit/config.toml` to repository
- [ ] Enable GitHub Actions with write permissions
- [ ] Test GitHub Actions workflow manually
- [ ] Deploy app on Streamlit Cloud
- [ ] Verify dashboard URL works
- [ ] Confirm automatic updates work (wait 4 hours or trigger manually)
- [ ] Check GitHub Actions runs successfully every 4 hours

---

## 🎉 Success!

Your FinSight dashboard is now:
- ✅ **Live** at https://finsight-financial-intelligence-dashboard.streamlit.app/
- ✅ **Auto-updating** every 4 hours with fresh financial news
- ✅ **Fully automated** with no manual intervention needed

---

## 📞 Support

If you encounter issues:
1. Check GitHub Actions logs
2. Check Streamlit Cloud logs
3. Verify all files are in correct locations
4. Ensure GitHub permissions are correct

Happy tracking! 📈💹
