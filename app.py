"""
FinSight - Financial Intelligence Dashboard
Displays financial news and insights with automated data updates
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="FinSight - Financial Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .news-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .update-time {
        color: #666;
        font-size: 0.9rem;
        text-align: right;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=600)  # Cache for 10 minutes, then reload
def load_news_data():
    """Load financial news data from CSV with proper error handling"""
    try:
        csv_path = 'finance_news.csv'
        
        if not os.path.exists(csv_path):
            st.error(f"❌ Data file '{csv_path}' not found. Please run news_fetch.py first.")
            return pd.DataFrame()
        
        df = pd.read_csv(csv_path)
        
        # Convert date columns if they exist
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        elif 'published' in df.columns:
            df['date'] = pd.to_datetime(df['published'], errors='coerce')
        elif 'timestamp' in df.columns:
            df['date'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        return df
    
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return pd.DataFrame()

def display_header():
    """Display dashboard header"""
    st.markdown('<div class="main-header">📊 FinSight</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Financial Intelligence Dashboard</p>', unsafe_allow_html=True)
    st.markdown("---")

def display_metrics(df):
    """Display key metrics"""
    if df.empty:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📰 Total Articles", len(df))
    
    with col2:
        if 'date' in df.columns:
            today = datetime.now().date()
            today_count = len(df[df['date'].dt.date == today])
            st.metric("📅 Today's News", today_count)
        else:
            st.metric("📅 Today's News", "N/A")
    
    with col3:
        if 'category' in df.columns:
            categories = df['category'].nunique()
            st.metric("📑 Categories", categories)
        elif 'source' in df.columns:
            sources = df['source'].nunique()
            st.metric("📡 Sources", sources)
        else:
            st.metric("📑 Categories", "N/A")
    
    with col4:
        if 'date' in df.columns and not df['date'].isna().all():
            last_update = df['date'].max()
            st.metric("🔄 Last Update", last_update.strftime("%Y-%m-%d %H:%M") if pd.notna(last_update) else "N/A")
        else:
            st.metric("🔄 Last Update", "N/A")

def display_news_timeline(df):
    """Display news timeline visualization"""
    if df.empty or 'date' not in df.columns:
        return
    
    st.subheader("📈 News Timeline")
    
    # Group by date and count
    df_copy = df.copy()
    df_copy['date_only'] = df_copy['date'].dt.date
    timeline_data = df_copy.groupby('date_only').size().reset_index(name='count')
    
    fig = px.line(
        timeline_data, 
        x='date_only', 
        y='count',
        title='News Articles Over Time',
        labels={'date_only': 'Date', 'count': 'Number of Articles'}
    )
    fig.update_traces(line_color='#1f77b4', line_width=3)
    fig.update_layout(hovermode='x unified')
    
    st.plotly_chart(fig, use_container_width=True)

def display_category_distribution(df):
    """Display category distribution"""
    if df.empty:
        return
    
    category_col = None
    if 'category' in df.columns:
        category_col = 'category'
    elif 'source' in df.columns:
        category_col = 'source'
    elif 'topic' in df.columns:
        category_col = 'topic'
    
    if category_col:
        st.subheader(f"📊 Distribution by {category_col.title()}")
        
        category_counts = df[category_col].value_counts().reset_index()
        category_counts.columns = [category_col, 'count']
        
        fig = px.pie(
            category_counts, 
            values='count', 
            names=category_col,
            title=f'Articles by {category_col.title()}',
            hole=0.4
        )
        
        st.plotly_chart(fig, use_container_width=True)

def display_news_articles(df, max_articles=20):
    """Display news articles as cards"""
    if df.empty:
        st.warning("⚠️ No news data available. The news fetching script will update this automatically every 4 hours.")
        return
    
    st.subheader("📰 Latest Financial News")
    
    # Sort by date if available
    if 'date' in df.columns:
        df = df.sort_values('date', ascending=False)
    
    # Display articles
    for idx, row in df.head(max_articles).iterrows():
        with st.container():
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            
            # Title
            title = row.get('title', 'No title')
            st.markdown(f"### {title}")
            
            # Metadata
            metadata_parts = []
            if 'source' in row and pd.notna(row['source']):
                metadata_parts.append(f"📡 {row['source']}")
            if 'category' in row and pd.notna(row['category']):
                metadata_parts.append(f"📑 {row['category']}")
            if 'date' in row and pd.notna(row['date']):
                metadata_parts.append(f"📅 {row['date'].strftime('%Y-%m-%d %H:%M')}")
            
            if metadata_parts:
                st.markdown(" | ".join(metadata_parts))
            
            # Description/Summary
            if 'description' in row and pd.notna(row['description']):
                st.write(row['description'])
            elif 'summary' in row and pd.notna(row['summary']):
                st.write(row['summary'])
            elif 'content' in row and pd.notna(row['content']):
                # Show first 200 characters of content
                content_preview = str(row['content'])[:200] + "..." if len(str(row['content'])) > 200 else str(row['content'])
                st.write(content_preview)
            
            # Link
            if 'url' in row and pd.notna(row['url']):
                st.markdown(f"[🔗 Read more]({row['url']})")
            elif 'link' in row and pd.notna(row['link']):
                st.markdown(f"[🔗 Read more]({row['link']})")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("")

def display_sidebar():
    """Display sidebar with filters and info"""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/graph.png", width=80)
        st.title("FinSight")
        st.markdown("---")
        
        st.markdown("### ℹ️ About")
        st.info("""
        **FinSight** provides real-time financial news and market intelligence.
        
        🔄 **Auto-updates every 4 hours**
        📊 Comprehensive news coverage
        🎯 Curated financial insights
        """)
        
        st.markdown("---")
        st.markdown("### 🛠️ Settings")
        
        # Reload data button
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Data Info")
        
        csv_path = 'finance_news.csv'
        if os.path.exists(csv_path):
            file_modified = datetime.fromtimestamp(os.path.getmtime(csv_path))
            st.markdown(f"**Last file update:**  \n{file_modified.strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.markdown("---")
        st.caption("Built with ❤️ using Streamlit")
        st.caption("Deployed on Streamlit Cloud")

def main():
    """Main application function"""
    # Display sidebar
    display_sidebar()
    
    # Display header
    display_header()
    
    # Load data
    df = load_news_data()
    
    # Display metrics
    display_metrics(df)
    
    st.markdown("---")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📰 News Feed", "📊 Analytics", "📋 Data Table"])
    
    with tab1:
        display_news_articles(df)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            display_news_timeline(df)
        
        with col2:
            display_category_distribution(df)
    
    with tab3:
        st.subheader("📋 Raw Data")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"finsight_news_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data to display")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div class="update-time">Dashboard updates automatically every 4 hours via GitHub Actions</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
