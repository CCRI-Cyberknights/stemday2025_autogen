#!/bin/bash
# start_web_hub.sh - Launch the CTF student hub

echo "🚀 Starting the CCRI CTF Student Hub..."
cd "$(dirname "$0")" || exit 1

# === Function: Launch browser ===
launch_browser() {
    export DISPLAY=:0
    echo "🌐 Opening browser to http://localhost:5000..."
    xdg-open http://localhost:5000 >/dev/null 2>&1 &
}

# === Check if Flask server is already running on port 5000 ===
if lsof -i:5000 >/dev/null 2>&1; then
    echo "🌐 Web server already running on port 5000."
    launch_browser
    echo "✅ CCRI CTF Student Hub is ready!"
    exit 0
fi

echo "🌐 Starting web server on port 5000..."
export FLASK_APP=server.py

# === Start Flask: prefer pipx Flask if installed ===
if [ -x "$HOME/.local/share/pipx/venvs/flask/bin/flask" ]; then
    echo "📦 Using pipx Flask..."
    "$HOME/.local/share/pipx/venvs/flask/bin/flask" run --host=127.0.0.1 --port=5000 &
elif command -v flask >/dev/null 2>&1; then
    echo "📦 Using system Python Flask..."
    python3 -m flask run --host=127.0.0.1 --port=5000 &
else
    echo "❌ Flask not found. Please run setup_dev_env.sh first."
    exit 1
fi

sleep 2  # Give Flask a moment to start

# === Wait for Flask server to respond before launching browser ===
echo "⏳ Waiting for web server to start..."
for i in {1..10}; do
    if curl -s http://localhost:5000 >/dev/null 2>&1; then
        echo "🌐 Web server is up!"
        launch_browser
        echo "✅ CCRI CTF Student Hub is ready!"
        exit 0
    else
        sleep 1
    fi
done

echo "❌ Failed to start Flask web server. Check for errors above."
exit 1
