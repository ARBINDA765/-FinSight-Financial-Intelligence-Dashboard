# 📊 FinSight - Financial Intelligence Dashboard

> **Automated financial news dashboard with real-time updates every 4 hours**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://finsight-financial-intelligence-dashboard.streamlit.app/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Features

- 📰 **Real-time Financial News** - Aggregates news from multiple sources
- 🔄 **Auto-Updates Every 4 Hours** - GitHub Actions keeps data fresh
- 📊 **Interactive Dashboard** - Beautiful visualizations with Plotly
- 🎯 **News Timeline** - Track news volume over time
- 📈 **Category Analytics** - Distribution of news by source/category
- 💾 **Data Export** - Download news data as CSV
- 🚀 **Zero Maintenance** - Fully automated pipeline

---

## 🎥 Demo

**Live Dashboard:** https://finsight-financial-intelligence-dashboard.streamlit.app/

![Dashboard Preview](https://img.icons8.com/color/96/000000/graph.png)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│  GitHub Actions (Every 4 hours)                     │
│  ├─ Runs news_fetch.py                              │
│  ├─ Updates finance_news.csv                        │
│  └─ Commits & pushes to GitHub                      │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│  GitHub Repository                                   │
│  └─ finance_news.csv (updated data)                 │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│  Streamlit Cloud                                     │
│  ├─ Detects CSV changes                             │
│  ├─ Auto-reloads dashboard                          │
│  └─ Displays fresh news to users                    │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
FinSight-Financial-Intelligence-Dashboard/
├── .github/
│   └── workflows/
│       └── update_news.yml          # 🤖 GitHub Actions automation
├── .streamlit/
│   └── config.toml                  # ⚙️ Streamlit configuration
├── app.py                           # 🎨 Main dashboard application
├── news_fetch.py                    # 📡 News fetching script
├── finance_news.csv                 # 💾 News data (auto-updated)
├── requirements.txt                 # 📦 Python dependencies
├── DEPLOYMENT_GUIDE.md              # 📖 Detailed deployment steps
├── QUICK_START.md                   # 🚀 Quick start for local testing
├── README.md                        # 📝 This file
└── .gitignore                       # 🚫 Files to ignore
```

---

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/ARBINDA765/-FinSight-Financial-Intelligence-Dashboard.git
   cd -FinSight-Financial-Intelligence-Dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Fetch initial news data**
   ```bash
   python news_fetch.py
   ```

4. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   ```
   http://localhost:8501
   ```

📖 **Detailed guide:** See [QUICK_START.md](QUICK_START.md)

---

## 🌐 Deployment to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free tier available)

### Deployment Steps

1. **Upload deployment files** to your repository:
   - `.github/workflows/update_news.yml`
   - `.streamlit/config.toml`

2. **Enable GitHub Actions**:
   - Go to Settings → Actions → General
   - Enable "Read and write permissions"

3. **Deploy on Streamlit Cloud**:
   - Visit https://streamlit.io/cloud
   - Connect your GitHub repository
   - Deploy with `app.py` as the main file

4. **Done!** Your dashboard will be live at:
   ```
   https://finsight-financial-intelligence-dashboard.streamlit.app/
   ```

📖 **Complete guide:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 🔧 Configuration

### Update Frequency

Edit `.github/workflows/update_news.yml` to change the schedule:

```yaml
schedule:
  - cron: '0 */4 * * *'  # Every 4 hours
  # - cron: '0 */2 * * *'  # Every 2 hours
  # - cron: '0 9 * * *'    # Daily at 9 AM UTC
```

Use [crontab.guru](https://crontab.guru/) for custom schedules.

### News Sources

`news_fetch.py` fetches from:
- **Google News** (no API key required)
- **RSS Feeds** (Yahoo Finance, CNBC, FT)
- **NewsAPI** (optional, requires API key)
- **Alpha Vantage** (optional, requires API key)

### Adding API Keys

For more articles, add API keys:

**Local Development:**
```bash
export NEWS_API_KEY="your_key"
export ALPHA_VANTAGE_KEY="your_key"
```

**Streamlit Cloud:**
Add to app settings → Secrets:
```toml
NEWS_API_KEY = "your_key"
ALPHA_VANTAGE_KEY = "your_key"
```

**GitHub Actions:**
Add to repository Settings → Secrets → Actions

---

## 📊 Data Schema

`finance_news.csv` contains:

| Column       | Type     | Description                    |
|-------------|----------|--------------------------------|
| title       | string   | Article headline               |
| description | string   | Article summary                |
| url         | string   | Link to full article           |
| source      | string   | News source/publisher          |
| date        | datetime | Publication timestamp          |
| category    | string   | News category                  |
| image_url   | string   | Article thumbnail (optional)   |

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/) - Interactive dashboards
- **Visualization:** [Plotly](https://plotly.com/) - Interactive charts
- **Data Processing:** [Pandas](https://pandas.pydata.org/) - Data manipulation
- **Automation:** [GitHub Actions](https://github.com/features/actions) - Scheduled workflows
- **Deployment:** [Streamlit Cloud](https://streamlit.io/cloud) - Free hosting
- **News APIs:** NewsAPI, Alpha Vantage, RSS feeds

---

## 🐛 Troubleshooting

### Dashboard shows "No data"
- Run `python news_fetch.py` locally first
- Check if `finance_news.csv` exists and has data
- Verify GitHub Actions is running (Actions tab)

### GitHub Actions failing
- Check Actions logs for errors
- Verify "Read and write permissions" is enabled
- Ensure `requirements.txt` is up to date

### Streamlit not updating
- Check if CSV was actually updated on GitHub
- Streamlit Cloud may take 1-2 minutes to detect changes
- Try manually rebooting the app in Streamlit Cloud

### API rate limits
- Use RSS feeds (no API key needed) as primary source
- Free tiers: NewsAPI (100/day), Alpha Vantage (25/day)
- Reduce update frequency if hitting limits

---

## 📈 Future Enhancements

- [ ] Add sentiment analysis
- [ ] Include stock price charts
- [ ] Add email notifications for breaking news
- [ ] Implement search functionality
- [ ] Add more news sources
- [ ] Create mobile-responsive layouts
- [ ] Add dark mode theme

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**ARBINDA765**

- GitHub: [@ARBINDA765](https://github.com/ARBINDA765)
- Project: [FinSight Dashboard](https://github.com/ARBINDA765/-FinSight-Financial-Intelligence-Dashboard)

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [NewsAPI](https://newsapi.org/) for financial news data
- [Alpha Vantage](https://www.alphavantage.co/) for market data
- All RSS feed providers

---

## 📞 Support

If you encounter issues:

1. Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for troubleshooting
2. Review [QUICK_START.md](QUICK_START.md) for setup help
3. Open an [issue](https://github.com/ARBINDA765/-FinSight-Financial-Intelligence-Dashboard/issues) on GitHub

---

<div align="center">

**⭐ If you find this project helpful, please give it a star! ⭐**

Made with ❤️ and ☕

[Live Demo](https://finsight-financial-intelligence-dashboard.streamlit.app/) • [Report Bug](https://github.com/ARBINDA765/-FinSight-Financial-Intelligence-Dashboard/issues) • [Request Feature](https://github.com/ARBINDA765/-FinSight-Financial-Intelligence-Dashboard/issues)

</div>
