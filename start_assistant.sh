#!/bin/bash

# Multi-Model AI Development Assistant - Unified Launcher
# Starts: Ollama, faust-mcp analysis server, faust realtime server, Streamlit app

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAUST_MCP_DIR="$SCRIPT_DIR/tools/faust-mcp"
ASSISTANT_DIR="$SCRIPT_DIR/multi-model-AI-development-assistant"
FAUST_MCP_PORT=8765
FAUST_REALTIME_PORT=8000
FAUST_UI_PORT=8787
STREAMLIT_PORT=8501

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Multi-Model AI Development Assistant - Unified Start  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to check if port is in use
check_port() {
    lsof -i:$1 > /dev/null 2>&1
}

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down services...${NC}"

    # Kill faust-mcp server
    if [ ! -z "$FAUST_MCP_PID" ]; then
        kill $FAUST_MCP_PID 2>/dev/null || true
        echo "  Stopped faust-mcp analysis server"
    fi

    # Kill faust realtime server
    if [ ! -z "$FAUST_REALTIME_PID" ]; then
        kill $FAUST_REALTIME_PID 2>/dev/null || true
        echo "  Stopped faust realtime server"
    fi

    # Kill Streamlit
    if [ ! -z "$STREAMLIT_PID" ]; then
        kill $STREAMLIT_PID 2>/dev/null || true
        echo "  Stopped Streamlit app"
    fi

    echo -e "${GREEN}Cleanup complete${NC}"
}

trap cleanup EXIT

# 1. Check Ollama
echo -e "${YELLOW}[1/5] Checking Ollama...${NC}"
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}Ollama not found. Please install Ollama first.${NC}"
    echo "  Visit: https://ollama.ai/"
    exit 1
fi

if ! pgrep -x "ollama" > /dev/null && ! curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "  Starting Ollama..."
    ollama serve > /dev/null 2>&1 &
    sleep 2
fi
echo -e "${GREEN}  ✓ Ollama is running${NC}"

# 2. Check Faust
echo -e "${YELLOW}[2/5] Checking Faust compiler...${NC}"
FAUST_VERSION=""
if command -v faust &> /dev/null; then
    FAUST_VERSION=$(faust --version 2>/dev/null | head -1)
    echo -e "${GREEN}  ✓ $FAUST_VERSION${NC}"
else
    echo -e "${YELLOW}  ! Faust not found - using DawDreamer backend if available${NC}"
fi

# 3. Start faust-mcp analysis server
echo -e "${YELLOW}[3/5] Starting faust-mcp analysis server on port $FAUST_MCP_PORT...${NC}"

# Activate virtual environment for faust-mcp
if [ -f "$ASSISTANT_DIR/venv/bin/activate" ]; then
    source "$ASSISTANT_DIR/venv/bin/activate"
fi

if check_port $FAUST_MCP_PORT; then
    echo -e "${GREEN}  ✓ Port $FAUST_MCP_PORT already in use (server may be running)${NC}"
    FAUST_MCP_RUNNING=true
else
    FAUST_MCP_RUNNING=false
    if [ -d "$FAUST_MCP_DIR" ]; then
        cd "$FAUST_MCP_DIR"

        # Create tmp directory if needed
        mkdir -p tmp

        # Detect backend
        if command -v faust &> /dev/null && command -v g++ &> /dev/null; then
            FAUST_SERVER="faust_server.py"
            echo "  Using C++ compilation backend"
        elif python3 -c "import dawDreamer" 2>/dev/null || python3 -c "import dawdreamer" 2>/dev/null; then
            FAUST_SERVER="faust_server_daw.py"
            echo "  Using DawDreamer backend"
        else
            echo -e "${RED}  No FAUST backend available!${NC}"
            echo "  Install either:"
            echo "    1. Faust compiler + g++ (recommended)"
            echo "    2. pip install dawDreamer"
            echo -e "${YELLOW}  Continuing without faust-mcp...${NC}"
            FAUST_SERVER=""
        fi

        if [ ! -z "$FAUST_SERVER" ]; then
            # Start the selected server
            MCP_TRANSPORT=sse \
            MCP_HOST=127.0.0.1 \
            MCP_PORT=$FAUST_MCP_PORT \
            TMPDIR="$FAUST_MCP_DIR/tmp" \
            python3 "$FAUST_SERVER" > "$FAUST_MCP_DIR/server.log" 2>&1 &

            FAUST_MCP_PID=$!

            # Wait for server to start (up to 5 seconds)
            for i in {1..10}; do
                if check_port $FAUST_MCP_PORT; then
                    break
                fi
                sleep 0.5
            done

            if check_port $FAUST_MCP_PORT; then
                echo -e "${GREEN}  ✓ faust-mcp server started (PID: $FAUST_MCP_PID)${NC}"
                FAUST_MCP_RUNNING=true
            else
                echo -e "${RED}  ✗ Failed to start faust-mcp server${NC}"
                echo "    Check log: $FAUST_MCP_DIR/server.log"
                FAUST_MCP_PID=""
            fi
        fi
    else
        echo -e "${YELLOW}  ! faust-mcp not found at $FAUST_MCP_DIR${NC}"
        echo "    Clone it with: git clone https://github.com/sletz/faust-mcp.git tools/faust-mcp"
    fi
fi

# 4. Start faust-mcp realtime server (if node-web-audio-api is available)
echo -e "${YELLOW}[4/5] Starting faust-mcp realtime server on port $FAUST_REALTIME_PORT...${NC}"
FAUST_REALTIME_RUNNING=false

if check_port $FAUST_REALTIME_PORT; then
    echo -e "${GREEN}  ✓ Port $FAUST_REALTIME_PORT already in use (server may be running)${NC}"
    FAUST_REALTIME_RUNNING=true
else
    WEBAUDIO_DIR="$FAUST_MCP_DIR/external/node-web-audio-api"
    if [ -d "$WEBAUDIO_DIR" ] && [ -f "$FAUST_MCP_DIR/faust_realtime_server.py" ]; then
        cd "$FAUST_MCP_DIR"

        # Check if node-web-audio-api is built
        if [ -d "$WEBAUDIO_DIR/node_modules" ]; then
            echo "  Using WebAudio realtime backend"

            # Start the realtime server with UI
            WEBAUDIO_ROOT="$WEBAUDIO_DIR" \
            MCP_TRANSPORT=sse \
            MCP_HOST=127.0.0.1 \
            MCP_PORT=$FAUST_REALTIME_PORT \
            FAUST_UI_PORT=$FAUST_UI_PORT \
            python3 faust_realtime_server.py > "$FAUST_MCP_DIR/realtime_server.log" 2>&1 &

            FAUST_REALTIME_PID=$!

            # Wait for server to start (up to 5 seconds)
            for i in {1..10}; do
                if check_port $FAUST_REALTIME_PORT; then
                    break
                fi
                sleep 0.5
            done

            if check_port $FAUST_REALTIME_PORT; then
                echo -e "${GREEN}  ✓ faust realtime server started (PID: $FAUST_REALTIME_PID)${NC}"
                echo -e "${GREEN}  ✓ faust-ui available at http://localhost:$FAUST_UI_PORT/${NC}"
                FAUST_REALTIME_RUNNING=true
            else
                echo -e "${RED}  ✗ Failed to start realtime server${NC}"
                echo "    Check log: $FAUST_MCP_DIR/realtime_server.log"
                FAUST_REALTIME_PID=""
            fi
        else
            echo -e "${YELLOW}  ! node-web-audio-api not built${NC}"
            echo "    Run: cd $WEBAUDIO_DIR && npm install && npm run build"
        fi
    else
        echo -e "${YELLOW}  ! Realtime server not available${NC}"
        echo "    Run: cd $FAUST_MCP_DIR && git submodule update --init --recursive"
    fi
fi

# 5. Start Streamlit app
echo -e "${YELLOW}[5/5] Starting Streamlit app on port $STREAMLIT_PORT...${NC}"
cd "$ASSISTANT_DIR"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "  Activated virtual environment"
fi

if check_port $STREAMLIT_PORT; then
    echo -e "${GREEN}  ✓ Port $STREAMLIT_PORT already in use${NC}"
    echo "  Open http://localhost:$STREAMLIT_PORT in your browser"
else
    streamlit run main.py --server.port $STREAMLIT_PORT > /dev/null 2>&1 &
    STREAMLIT_PID=$!
    sleep 3

    if check_port $STREAMLIT_PORT; then
        echo -e "${GREEN}  ✓ Streamlit started (PID: $STREAMLIT_PID)${NC}"
    else
        echo -e "${RED}  ✗ Failed to start Streamlit${NC}"
    fi
fi

# Summary
echo ""
if [ "$FAUST_MCP_RUNNING" = true ] && [ "$FAUST_REALTIME_RUNNING" = true ]; then
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                     All Services Started                     ║${NC}"
    echo -e "${GREEN}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║  Streamlit App:       http://localhost:$STREAMLIT_PORT                    ║${NC}"
    echo -e "${GREEN}║  FAUST Analysis:      http://localhost:$FAUST_MCP_PORT/sse (offline)       ║${NC}"
    echo -e "${GREEN}║  FAUST Realtime:      http://localhost:$FAUST_REALTIME_PORT/sse (live audio)    ║${NC}"
    echo -e "${GREEN}║  FAUST UI:            http://localhost:$FAUST_UI_PORT/ (param sliders)    ║${NC}"
    echo -e "${GREEN}║  Ollama API:          http://localhost:11434                  ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
elif [ "$FAUST_MCP_RUNNING" = true ]; then
    echo -e "${YELLOW}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║               Services Started (realtime unavailable)        ║${NC}"
    echo -e "${YELLOW}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║  Streamlit App:       http://localhost:$STREAMLIT_PORT                    ║${NC}"
    echo -e "${GREEN}║  FAUST Analysis:      http://localhost:$FAUST_MCP_PORT/sse                 ║${NC}"
    echo -e "${YELLOW}║  FAUST Realtime:      NOT RUNNING (see setup instructions)   ║${NC}"
    echo -e "${GREEN}║  Ollama API:          http://localhost:11434                  ║${NC}"
    echo -e "${YELLOW}╚══════════════════════════════════════════════════════════════╝${NC}"
else
    echo -e "${YELLOW}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║                Services Started (with warnings)              ║${NC}"
    echo -e "${YELLOW}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║  Streamlit App:       http://localhost:$STREAMLIT_PORT                    ║${NC}"
    echo -e "${YELLOW}║  FAUST Analysis:      FAILED (check server.log)              ║${NC}"
    echo -e "${YELLOW}║  FAUST Realtime:      NOT RUNNING                            ║${NC}"
    echo -e "${GREEN}║  Ollama API:          http://localhost:11434                  ║${NC}"
    echo -e "${YELLOW}╚══════════════════════════════════════════════════════════════╝${NC}"
fi
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Keep script running
wait
