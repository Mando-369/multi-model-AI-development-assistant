#!/bin/bash

echo "🔧 Launching Development Mode with Claude Code"
echo "=============================================="

# This is for when you want to optimize the system
cd /path/to/multi-model-AI-development-assistant

# Check if Claude Code is initialized
if [ ! -f "claude.md" ]; then
    echo "Initializing Claude Code..."
    claude init
fi

# Launch Claude Code for development
echo "Starting Claude Code development assistant..."
echo "Use agents to optimize the system:"
echo "  /agent system-optimizer"
echo "  /agent hrm-integrator"
echo ""

claude