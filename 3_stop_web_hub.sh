#!/bin/bash
echo "🛑 Stopping CCRI CTF Student Hub..."

# Kill flask run
pkill -f "flask run --host=127.0.0.1 --port=5000" 2>/dev/null

# Kill python3 server.py if running
pkill -f "python3 server.py" 2>/dev/null

# Kill gunicorn (if we ever use it)
pkill -f "gunicorn.*server:app" 2>/dev/null

# Check if anything is still running on port 5000
if lsof -i:5000 >/dev/null 2>&1; then
    echo "⚠️ Server processes still running on port 5000."
else
    echo "✅ Server stopped."
fi
