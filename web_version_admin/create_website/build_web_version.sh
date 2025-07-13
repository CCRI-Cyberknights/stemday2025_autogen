#!/bin/bash
# build_web_version.sh – Builds student web version & injects start/stop scripts

set -e

# === Paths ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/../../" && pwd)"
STUDENT_DIR="$BASE_DIR/web_version"

echo "🚀 Building Web Version"
echo "📂 Script dir: $SCRIPT_DIR"
echo "📂 Base dir:   $BASE_DIR"

# === Validate directory structure ===
validate_structure() {
    local missing=()

    [[ ! -d "$BASE_DIR/web_version_admin" ]] && missing+=("web_version_admin/")
    [[ ! -d "$BASE_DIR/challenges" ]] && missing+=("challenges/")
    [[ ! -f "$BASE_DIR/web_version_admin/challenges.json" ]] && missing+=("challenges.json")

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "❌ Missing required files/directories:"
        printf "   %s\n" "${missing[@]}"
        exit 1
    fi
}

# === Build process using Python ===
run_build() {
    python3 - << 'EOF'
import json, base64, os, shutil, stat

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
ADMIN_DIR = os.path.join(BASE_DIR, "web_version_admin")
STUDENT_DIR = os.path.join(BASE_DIR, "web_version")
CHALLENGES_DIR = os.path.join(BASE_DIR, "challenges")
ENCODE_KEY = "CTF4EVER"

def xor_encode(plaintext, key):
    """XOR + Base64 encode a plaintext flag."""
    encoded_bytes = bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(plaintext)])
    return base64.b64encode(encoded_bytes).decode()

# Clean & prepare student dir
if os.path.exists(STUDENT_DIR):
    shutil.rmtree(STUDENT_DIR)
os.makedirs(STUDENT_DIR)

# Process challenges.json
with open(os.path.join(ADMIN_DIR, "challenges.json"), "r") as f:
    admin_data = json.load(f)

student_data = {}
for cid, meta in admin_data.items():
    folder_path = meta["folder"].replace("../", "").lstrip("./")
    student_data[cid] = {
        "name": meta["name"],
        "folder": os.path.join("..", folder_path),
        "script": meta.get("script", ""),
        "flag": xor_encode(meta["flag"], ENCODE_KEY)
    }

# Write new challenges.json
with open(os.path.join(STUDENT_DIR, "challenges.json"), "w") as f:
    json.dump(student_data, f, indent=2)

# Copy static & templates
for folder in ["templates", "static"]:
    src = os.path.join(ADMIN_DIR, folder)
    dst = os.path.join(STUDENT_DIR, folder)
    if os.path.exists(src):
        shutil.copytree(src, dst)

# Copy server.py
shutil.copy2(os.path.join(ADMIN_DIR, "server.py"), os.path.join(STUDENT_DIR, "server.py"))
EOF
}

# === Inject start_web_hub.sh ===
add_start_web_hub() {
    echo "🚀 Generating start_web_hub.sh in web_version..."
    cat << 'EOL' > "$STUDENT_DIR/start_web_hub.sh"
#!/bin/bash
echo "🌐 Starting CCRI CTF Student Hub..."

cd "$(dirname "$(realpath "$0")")" || exit 1

# Start server if not running
if pgrep -f "python3 server.py" >/dev/null 2>&1; then
    echo "✅ Server already running."
else
    nohup python3 server.py >/dev/null 2>&1 &
    echo "✅ Server launched at http://127.0.0.1:5000"
fi

# Launch browser, fully detached
if command -v xdg-open >/dev/null 2>&1; then
    echo "🌐 Opening browser..."
    setsid xdg-open "http://127.0.0.1:5000" >/dev/null 2>&1 &
else
    echo "⚠️ Could not detect browser. Open http://127.0.0.1:5000 manually."
fi

sleep 2
EOL
    chmod +x "$STUDENT_DIR/start_web_hub.sh"
}

# === Inject stop_web_hub.sh ===
add_stop_web_hub() {
    echo "🛑 Generating stop_web_hub.sh in web_version..."
    cat << 'EOL' > "$STUDENT_DIR/stop_web_hub.sh"
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
EOL
    chmod +x "$STUDENT_DIR/stop_web_hub.sh"
}

# === Main ===
main() {
    validate_structure
    run_build
    add_start_web_hub
    add_stop_web_hub
    echo "🎉 Build complete! Web version is ready in: $STUDENT_DIR"
}

main "$@"
