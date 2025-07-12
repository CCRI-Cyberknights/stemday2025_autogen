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
else
    echo "🌐 Starting web server on port 5000..."
    if [ -f "server.pyc" ]; then
        python3 server.pyc >/dev/null 2>&1 &
    else
        python3 server.py >/dev/null 2>&1 &
    fi
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
