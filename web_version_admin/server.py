try:
    from flask import Flask, render_template, request, jsonify, Markup, send_from_directory
except ImportError:
    from flask import Flask, render_template, request, jsonify, send_from_directory
    from markupsafe import Markup

import subprocess
import json
import os
import base64
import threading
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from ChallengeList import ChallengeList
import markdown

# === Handle PyInstaller path resolution ===
import sys
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === App Initialization ===
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

DEBUG_MODE = os.environ.get("CCRI_DEBUG", "0") == "1"
logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.INFO)

# === Load Challenges ===
challenges_path = os.path.join(BASE_DIR, "challenges.json")
try:
    print(f"Loading challenges from {challenges_path}...")
    challenges = ChallengeList(challenges_file=challenges_path)
    print(f"Loaded {challenges.numOfChallenges} challenges successfully.")
except FileNotFoundError:
    print(f"❌ ERROR: Could not find '{challenges_path}'!")
    exit(1)
except json.JSONDecodeError:
    print(f"❌ ERROR: '{challenges_path}' contains invalid JSON!")
    exit(1)

# === Helper: XOR Decode ===
def xor_decode(encoded_base64, key):
    decoded_bytes = base64.b64decode(encoded_base64)
    return ''.join(
        chr(b ^ ord(key[i % len(key)]))
        for i, b in enumerate(decoded_bytes)
    )

# === Routes ===
@app.route('/')
def index():
    return render_template('index.html', challenges=challenges)

@app.route('/challenge/<challenge_id>')
def challenge_view(challenge_id):
    selectedChallenge = challenges.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return "Challenge not found", 404

    folder = selectedChallenge.getFolder()
    readme_html = ""
    readme_path = os.path.join(folder, 'README.txt')
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                raw_readme = f.read()
                readme_html = Markup(markdown.markdown(raw_readme))
        except Exception as e:
            readme_html = f"<p><strong>Error loading README:</strong> {e}</p>"

    file_list = [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
        and f != "README.txt"
        and not f.startswith(".")
    ]

    return render_template('challenge.html', challenge=selectedChallenge, readme=readme_html, files=file_list)

@app.route('/challenge/<challenge_id>/file/<path:filename>')
def get_challenge_file(challenge_id, filename):
    selectedChallenge = challenges.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return "Challenge not found", 404

    folder = selectedChallenge.getFolder()
    if not os.path.isfile(os.path.join(folder, filename)):
        return "File not found", 404

    return send_from_directory(folder, filename)

@app.route('/submit_flag/<challenge_id>', methods=['POST'])
def submit_flag(challenge_id):
    data = request.get_json()
    submitted_flag = data.get('flag', '').strip().upper()

    selectedChallenge = challenges.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    correct_flag = selectedChallenge.getFlag().strip().upper()

    if submitted_flag == correct_flag:
        selectedChallenge.setComplete()
        if selectedChallenge.getId() not in challenges.completed_challenges:
            challenges.completed_challenges.append(selectedChallenge.getId())
        print(f"✅ Challenge '{selectedChallenge.getName()}' completed.")
        return jsonify({"status": "correct"})
    else:
        print(f"❌ Incorrect flag for '{selectedChallenge.getName()}'.")
        return jsonify({"status": "incorrect"})

@app.route('/open_folder/<challenge_id>', methods=['POST'])
def open_folder(challenge_id):
    selectedChallenge = challenges.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    folder = selectedChallenge.getFolder()
    try:
        subprocess.Popen(['xdg-open', folder], shell=False)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/run_script/<challenge_id>', methods=['POST'])
def run_script(challenge_id):
    selectedChallenge = challenges.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    script_path = os.path.join(selectedChallenge.getFolder(), selectedChallenge.getScript())

    if not os.path.isfile(script_path):
        return jsonify({"status": "error", "message": f"Script '{selectedChallenge.getScript()}' not found."}), 404

    try:
        # === Detect if running on Parrot OS and prefer parrot-terminal ===
        if os.path.exists("/etc/parrot"):  # Parrot-specific marker file
            print("🐦 Detected Parrot OS. Forcing parrot-terminal.")
            subprocess.Popen([
                "parrot-terminal",
                "--working-directory", selectedChallenge.getFolder(),
                "-e", f"bash \"{script_path}\""
            ], shell=False)
            return jsonify({"status": "success"})

        # === Fallback for non-Parrot distros ===
        fallback_terminals = ["gnome-terminal", "konsole", "xfce4-terminal", "lxterminal"]
        for term in fallback_terminals:
            if subprocess.call(["which", term], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                subprocess.Popen([
                    term,
                    "--working-directory", selectedChallenge.getFolder(),
                    "-e", f"bash \"{script_path}\""
                ], shell=False)
                return jsonify({"status": "success"})

        return jsonify({"status": "error", "message": "No supported terminal emulator found."}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# === Simulated Open Ports ===
FAKE_FLAGS = {
    8004: "NMAP-PORT-4312",
    8023: "SCAN-4312-PORT",
    8047: "CCRI-SCAN-8472",  # ✅ REAL FLAG
    8072: "OPEN-SERVICE-9281",
    8095: "HTTP-7721-SERVER"
}
SERVICE_NAMES = {
    8004: "configd",
    8023: "metricsd",
    8047: "sysmon-api",
    8072: "update-agent",
    8095: "metrics-gateway"
}

class PortHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = ALL_PORTS.get(self.server.server_port, "Connection refused")
        banner = f"👋 Welcome to {SERVICE_NAMES.get(self.server.server_port, 'http')} Service\n\n"
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.send_header("Server", SERVICE_NAMES.get(self.server.server_port, "http"))
        self.end_headers()
        self.wfile.write((banner + response).encode("utf-8"))

    def log_message(self, format, *args):
        return  # Silence logs

def start_fake_service(port):
    try:
        server = HTTPServer(('0.0.0.0', port), PortHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print(f"🛰️  Simulated service running on port {port} ({SERVICE_NAMES.get(port, 'http')})")
    except OSError as e:
        print(f"❌ Could not bind port {port}: {e}")

for port in FAKE_FLAGS:
    start_fake_service(port)

if __name__ == '__main__':
    print("🌐 Student hub running on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
