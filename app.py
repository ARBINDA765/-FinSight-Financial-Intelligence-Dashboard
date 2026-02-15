import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="FinSight", layout="wide")

# Load data
DATA_PATH = Path("data/finance_news.csv")
st.title("📊 FinSight – Financial Intelligence Dashboard")

if not DATA_PATH.exists():
    st.warning("Run `news_fetch.py` first to generate data.")
    st.stop()

df = pd.read_csv(DATA_PATH)

# Last refresh time (file modified time)
last_refresh_ts = datetime.fromtimestamp(DATA_PATH.stat().st_mtime)
st.markdown(f"**Last refresh:** {last_refresh_ts.strftime('%Y-%m-%d %H:%M:%S')} (local)")

# Styling: bold green headers, light green background, larger fonts
st.markdown(
    """
    <style>
    .fin-table thead th {
        font-weight: 700 !important;
        color: #1b5e20 !important; /* dark green */
        background-color: #e8f5e9 !important; /* light green */
        font-size: 16px !important;
    }
    .fin-table td {
        font-size: 14px !important;
        padding: 8px !important;
    }
    .stMetric > div {
        font-size:18px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar filters as dropdowns
st.sidebar.header("🔎 Filters")
topic_options = ["All"] + sorted(df["topic"].dropna().unique().tolist())
source_options = ["All"] + sorted(df["source"].dropna().unique().tolist())

topic_sel = st.sidebar.selectbox("Topic", topic_options, index=0)
source_sel = st.sidebar.selectbox("Source", source_options, index=0)
keyword = st.sidebar.text_input("Keyword Search")

# Apply filters
filtered = df.copy()
if topic_sel != "All":
    filtered = filtered[filtered["topic"] == topic_sel]
if source_sel != "All":
    filtered = filtered[filtered["source"] == source_sel]
if keyword:
    filtered = filtered[filtered["title"].str.contains(keyword, case=False, na=False) | filtered.get("overview", "").str.contains(keyword, case=False, na=False)]

# KPI cards
col1, col2, col3 = st.columns(3)
col1.metric("Total News", len(filtered))
col2.metric("Unique Sources", int(filtered["source"].nunique()))
col3.metric("Topics", int(filtered["topic"].nunique()))

# Reorder columns: topic, title, link, then others
preferred = ["topic", "title", "overview", "link", "source", "published", "date_loaded"]
cols = [c for c in preferred if c in filtered.columns] + [c for c in filtered.columns if c not in preferred]
display_df = filtered[cols].copy()

# Make link column clickable
if "link" in display_df.columns:
    display_df["link"] = display_df["link"].apply(lambda x: f'<a href="{x}" target="_blank">Open</a>' if pd.notna(x) and x else "")

# Render table as HTML to allow styling and clickable links
html_table = display_df.to_html(classes="fin-table", escape=False, index=False)
st.markdown(html_table, unsafe_allow_html=True)

# Detailed interactive view using expanders
st.subheader("Detailed Articles")
for _, row in filtered.sort_values(by="published", ascending=False).iterrows():
    title = row.get("title", "")
    topic = row.get("topic", "")
    src = row.get("source", "")
    link = row.get("link", "")
    overview = row.get("overview", "")
    with st.expander(f"{topic} — {title}"):
        st.write(f"**Source:** {src}")
        if link:
            st.markdown(f"[Open Article]({link})")
        if overview:
            st.write(overview)
        st.write(f"Published: {row.get('published', '')}")
