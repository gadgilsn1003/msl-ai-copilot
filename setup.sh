#!/usr/bin/env bash
# =============================================================================
# MSL AI Copilot — Local Setup & Launch Script
# =============================================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== MSL AI Copilot Setup ===${NC}"

# 1. Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED="3.10"
if python3 -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)"; then
    echo -e "${GREEN}[OK] Python ${PYTHON_VERSION} detected${NC}"
else
    echo -e "${RED}[ERROR] Python 3.10+ required. Found: ${PYTHON_VERSION}${NC}"
    exit 1
fi

# 2. Create virtual environment
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}[INFO] Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

# 3. Activate virtual environment
echo -e "${YELLOW}[INFO] Activating virtual environment...${NC}"
source .venv/bin/activate

# 4. Upgrade pip
pip install --upgrade pip --quiet

# 5. Install dependencies
echo -e "${YELLOW}[INFO] Installing dependencies...${NC}"
pip install -r requirements.txt --quiet
echo -e "${GREEN}[OK] Dependencies installed${NC}"

# 6. Setup environment file
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}[WARN] .env file created from .env.example"
        echo -e "       Please edit .env and add your API keys before launching!${NC}"
    fi
else
    echo -e "${GREEN}[OK] .env file found${NC}"
fi

# 7. Check for required env vars
if grep -q "your_openai_api_key_here" .env 2>/dev/null; then
    echo -e "${RED}[WARN] OpenAI API key not configured in .env${NC}"
    echo -e "       Edit .env and set OPENAI_API_KEY before launching."
fi

# 8. Create data directory
mkdir -p data
echo -e "${GREEN}[OK] Data directory ready${NC}"

# 9. Launch the app
echo ""
echo -e "${GREEN}=== Launching MSL AI Copilot ===${NC}"
echo -e "${YELLOW}   URL: http://localhost:8501${NC}"
echo ""

streamlit run app.py \
    --server.port 8501 \
    --browser.gatherUsageStats false
