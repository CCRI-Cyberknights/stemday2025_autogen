#!/bin/bash
echo "🛑 Stopping CCRI CTF Student Hub..."
pkill -f "flask run --host=127.0.0.1 --port=5000" && \
    echo "✅ Server stopped." || echo "⚠️ No server running."
