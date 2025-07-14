#!/bin/bash
echo "🛑 Stopping CCRI CTF Student Hub..."

# === Kill server.pyc and server.py processes ===
pkill -f "server.pyc" 2>/dev/null && echo "✅ Killed server.pyc" || echo "⚠️ No server.pyc process running."
pkill -f "server.py"  2>/dev/null && echo "✅ Killed server.py"  || echo "⚠️ No server.py process running."

# === Kill any Flask/Gunicorn processes on port 5000 ===
if lsof -i:5000 >/dev/null 2>&1; then
    echo "🔪 Killing processes on port 5000..."
    lsof -ti:5000 | xargs kill -9
    echo "✅ Port 5000 cleared."
else
    echo "⚠️ No processes found on port 5000."
fi

# === Kill all simulated services on ports 8000–8100 ===
ports_killed=0
for port in $(seq 8000 8100); do
    if lsof -i:$port >/dev/null 2>&1; then
        lsof -ti:$port | xargs kill -9
        ports_killed=$((ports_killed + 1))
    fi
done

if [[ $ports_killed -gt 0 ]]; then
    echo "✅ Cleared $ports_killed simulated service(s) on ports 8000–8100."
else
    echo "⚠️ No simulated services running on ports 8000–8100."
fi

echo "🎯 All cleanup complete."
