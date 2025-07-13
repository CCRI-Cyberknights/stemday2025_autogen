#!/bin/bash
# start_web_hub.sh - Launch the CTF student hub

echo "🚀 Starting the CCRI CTF Student Hub..."
cd "$(dirname "$0")" || exit 1

# === Function: Launch browser ===
launch_browser() {
    export DISPLAY=:0
    echo "🌐 Opening browser to http://localhost:5000..."
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open http://localhost:5000 >/dev/null 2>&1 &
    elif command -v sensible-browser >/dev/null 2>&1; then
        sensible-browser http://localhost:5000 >/dev/null 2>&1 &
    elif command -v firefox >/dev/null 2>&1; then
        firefox http://localhost:5000 >/dev/null 2>&1 &
    else
        echo "⚠️ Could not find a browser to launch. Please open http://localhost:5000 manually."
    fi
}

# === Function: Start Flask server ===
start_flask_server() {
    if command -v pipx >/dev/null 2>&1 && pipx list | grep -q flask; then
        echo "🌐 Starting Flask server using pipx..."
        export FLASK_APP=server.py
        pipx run flask run --host=127.0.0.1 --port=5000 >/dev/null 2>&1 &
    elif python3 -m flask --version >/dev/null 2>&1; then
        echo "🌐 Starting Flask server using system Python..."
        export FLASK_APP=server.py
        python3 -m flask run --host=127.0.0.1 --port=5000 >/dev/null 2>&1 &
    elif [ -f "server.pyc" ]; then
        echo "🌐 Starting server.pyc with system Python..."
        python3 server.pyc >/dev/null 2>&1 &
    elif [ -f "server.py" ]; then
        echo "🌐 Starting server.py with system Python..."
        python3 server.py >/dev/null 2>&1 &
    else
        echo "❌ Could not find a way to start the Flask server!"
        exit 1
    fi
}

# === Check if Flask server is already running on port 5000 ===
if lsof -i:5000 >/dev/null 2>&1; then
    echo "🌐 Web server already running on port 5000."
    launch_browser
    echo "✅ CCRI CTF Student Hub is ready!"
    exit 0
else
    echo "🌐 Starting web server on port 5000..."
    start_flask_server
    sleep 2  # Give it a moment to start
fi

# === Wait for Flask server to respond before launching browser ===
echo "⏳ Waiting for web server to start..."
for i in {1..10}; do
    if curl -s http://localhost:5000 >/dev/null 2>&1; then
        echo "🌐 Web server is up!"
        break
    else
        sleep 1
    fi
done

launch_browser
echo "✅ CCRI CTF Student Hub is ready!"

# === Keep script alive briefly for desktop launcher ===
sleep 2
