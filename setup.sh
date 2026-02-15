#!/bin/bash

# FinSight - Automated Setup Script
# This script sets up your repository for deployment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print header
echo -e "${BOLD}${BLUE}"
echo "============================================================"
echo "  FinSight - Automated Setup for Deployment"
echo "============================================================"
echo -e "${NC}"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not in a git repository. Please run this script from your repository root.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Git repository detected${NC}\n"

# Create directories
echo "Creating directory structure..."
mkdir -p .github/workflows
mkdir -p .streamlit
echo -e "${GREEN}✓ Directories created${NC}\n"

# Check if files already exist
OVERWRITE=false
if [ -f ".github/workflows/update_news.yml" ] || [ -f ".streamlit/config.toml" ]; then
    echo -e "${YELLOW}Warning: Some deployment files already exist.${NC}"
    read -p "Do you want to overwrite them? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        OVERWRITE=true
    else
        echo -e "${YELLOW}Skipping file creation. Using existing files.${NC}\n"
    fi
fi

# Create or update requirements.txt
echo "Checking requirements.txt..."
if [ ! -f "requirements.txt" ] || [ "$OVERWRITE" = true ]; then
    cat > requirements.txt << 'EOF'
# Core Dependencies
streamlit>=1.31.0
pandas>=2.0.0
numpy>=1.24.0

# Data Visualization
plotly>=5.18.0
matplotlib>=3.7.0
seaborn>=0.12.0

# News Fetching
requests>=2.31.0
beautifulsoup4>=4.12.0
feedparser>=6.0.0
python-dateutil>=2.8.0

# Utilities
pytz>=2023.3
EOF
    echo -e "${GREEN}✓ requirements.txt created${NC}"
else
    echo -e "${YELLOW}⚠ requirements.txt already exists (not modified)${NC}"
fi

# Install dependencies
echo -e "\n${BOLD}Installing Python dependencies...${NC}"
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Run verification
if [ -f "verify_setup.py" ]; then
    echo -e "${BOLD}Running setup verification...${NC}\n"
    python verify_setup.py
else
    echo -e "${YELLOW}⚠ verify_setup.py not found, skipping verification${NC}"
fi

# Test news fetch
echo -e "\n${BOLD}Testing news fetch...${NC}"
if [ -f "news_fetch.py" ]; then
    python news_fetch.py
    if [ -f "finance_news.csv" ]; then
        echo -e "${GREEN}✓ News data fetched successfully${NC}"
        lines=$(wc -l < finance_news.csv)
        echo -e "${GREEN}  CSV contains $lines lines${NC}"
    else
        echo -e "${RED}✗ Failed to create finance_news.csv${NC}"
    fi
else
    echo -e "${YELLOW}⚠ news_fetch.py not found${NC}"
fi

# Git status
echo -e "\n${BOLD}Git Status:${NC}"
git status --short

# Commit changes
echo -e "\n${YELLOW}Ready to commit changes?${NC}"
read -p "Commit deployment files? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git add .github/ .streamlit/ requirements.txt finance_news.csv .gitignore 2>/dev/null || true
    git commit -m "Setup: Add deployment configuration for Streamlit Cloud"
    echo -e "${GREEN}✓ Changes committed${NC}"
    
    read -p "Push to GitHub? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push
        echo -e "${GREEN}✓ Changes pushed to GitHub${NC}"
    fi
fi

# Final instructions
echo -e "\n${BOLD}${GREEN}============================================================"
echo "  Setup Complete!"
echo "============================================================${NC}\n"

echo "Next steps:"
echo "1. ${BOLD}Enable GitHub Actions:${NC}"
echo "   - Go to: Settings → Actions → General"
echo "   - Enable 'Read and write permissions'"
echo ""
echo "2. ${BOLD}Deploy to Streamlit Cloud:${NC}"
echo "   - Visit: https://streamlit.io/cloud"
echo "   - Connect your repository"
echo "   - Deploy with app.py"
echo ""
echo "3. ${BOLD}Your dashboard will be live at:${NC}"
echo "   https://finsight-financial-intelligence-dashboard.streamlit.app/"
echo ""
echo "📖 For detailed instructions, see: DEPLOYMENT_GUIDE.md"
echo ""
