#!/bin/bash
# start_web_hub.sh - Launch the CTF student hub
# Ensure we have access to the graphical environment
export DISPLAY=:0

echo "🚀 Starting the CCRI CTF Student Hub..."
cd "$(dirname "$0")" || exit 1

# === Locate server.py ===
if [ -f "server.py" ]; then
    export FLASK_APP="server.py"
elif [ -f "web_version_admin/server.py" ]; then
    echo "📂 Adjusting FLASK_APP path for parent directory..."
    export FLASK_APP="web_version_admin/server.py"
    cd "web_version_admin" || {
        echo "❌ Failed to change to web_version_admin directory!"
        exit 1
    }
else
    echo "❌ server.py not found! Cannot start web hub."
    exit 1
fi

# === Check if Flask server is already running ===
if lsof -i:5000 >/dev/null 2>&1; then
    echo "🌐 Web server already running on port 5000."
else
    echo "🌐 Starting web server on port 5000..."
    if [ -x "$HOME/.local/share/pipx/venvs/flask/bin/flask" ]; then
        echo "📦 Using pipx Flask..."
        nohup "$HOME/.local/share/pipx/venvs/flask/bin/flask" run --host=127.0.0.1 --port=5000 >/dev/null 2>&1 &
    else
        echo "📦 Using system Flask..."
        nohup python3 -m flask run --host=127.0.0.1 --port=5000 >/dev/null 2>&1 &
    fi
    sleep 2  # Give Flask a moment to start
fi

# === Launch browser ===
echo "🌐 Opening browser to http://localhost:5000..."
if command -v firefox >/dev/null 2>&1; then
    echo "➡️ Launching Firefox directly (detached)..."
    nohup firefox http://localhost:5000 >/dev/null 2>&1 &
else
    echo "⚠️ Could not detect Firefox. Please open http://localhost:5000 manually."
fi

echo "✅ CCRI CTF Student Hub is ready!"

# === Keep script alive briefly for desktop launcher environments ===
sleep 3
