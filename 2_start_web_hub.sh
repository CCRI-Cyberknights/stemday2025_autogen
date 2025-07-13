#!/bin/bash
echo "🌐 Starting CCRI CTF Student Hub..."

cd "$(dirname "$(realpath "$0")")" || exit 1

# Start server if not running
if pgrep -f "server.py" >/dev/null 2>&1; then
    echo "✅ Server already running."
else
    # Check if pipx Flask exists
    if [ -x "$HOME/.local/share/pipx/venvs/flask/bin/flask" ]; then
        echo "📦 Starting server with pipx Flask..."
        nohup "$HOME/.local/share/pipx/venvs/flask/bin/flask" run --host=127.0.0.1 --port=5000 >/dev/null 2>&1 &
    else
        echo "📦 Starting server with system Python..."
        nohup python3 server.py >/dev/null 2>&1 &
    fi
    echo "✅ Server launched at http://127.0.0.1:5000"
    sleep 2  # Wait briefly for server to come up
fi

# Launch browser, fallback if needed
echo "🌐 Opening browser to http://127.0.0.1:5000..."
if command -v xdg-open >/dev/null 2>&1; then
    setsid xdg-open "http://127.0.0.1:5000" >/dev/null 2>&1 &
elif command -v firefox >/dev/null 2>&1; then
    setsid firefox "http://127.0.0.1:5000" >/dev/null 2>&1 &
else
    echo "⚠️ Could not detect browser. Please open http://127.0.0.1:5000 manually."
fi

echo "✅ CCRI CTF Student Hub is ready!"
