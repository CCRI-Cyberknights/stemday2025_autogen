try:
    # Flask 2.x: Markup is inside flask
    from flask import Flask, render_template, request, jsonify, Markup
except ImportError:
    # Flask 3.x: Markup moved to markupsafe
    from flask import Flask, render_template, request, jsonify
    from markupsafe import Markup

import subprocess
import json
import os
import base64
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# New import for Markdown support
import markdown

app = Flask(__name__)


# === Docker Detection ===
def is_running_in_docker():
    """Detect if we're running inside a Docker container"""
    try:
        # Method 1: Check for .dockerenv file
        if os.path.exists('/.dockerenv'):
            return True

        # Method 2: Check cgroup info (Linux containers)
        if os.path.exists('/proc/1/cgroup'):
            with open('/proc/1/cgroup', 'r') as f:
                content = f.read()
                if 'docker' in content or 'containerd' in content:
                    return True

        # Method 3: Check if hostname looks like a container ID
        hostname = os.uname().nodename
        if len(hostname) == 12 and all(c in '0123456789abcdef' for c in hostname):
            return True

        # Method 4: Check environment variables
        if os.getenv('DOCKER_CONTAINER') or os.getenv('container'):
            return True

        return False
    except:
        return False


def get_server_config():
    """Get server configuration based on environment"""
    in_docker = is_running_in_docker()

    if in_docker:
        # In Docker: bind to all interfaces so host can access
        host = '0.0.0.0'
        debug = False
        print("🐳 Running in Docker container")
    else:
        # Native: bind to localhost only for security
        host = '127.0.0.1'
        debug = os.getenv('FLASK_DEBUG', '').lower() in ('1', 'true', 'yes')
        print("💻 Running natively on host")

    port = int(os.getenv('FLASK_PORT', 5000))

    return {
        'host': host,
        'port': port,
        'debug': debug,
        'in_docker': in_docker
    }


# === Hardcoded XOR Key ===
XOR_KEY = "CTF4EVER"

# === Load student challenges.json ===
with open('challenges.json', 'r') as f:
    challenges = json.load(f)


# === Helper: XOR Decode ===
def xor_decode(encoded_base64, key):
    decoded_bytes = base64.b64decode(encoded_base64)
    return ''.join(
        chr(b ^ ord(key[i % len(key)]))
        for i, b in enumerate(decoded_bytes)
    )


# === Flask Routes ===
@app.route('/')
def index():
    """Main grid of all challenges"""
    return render_template('index.html', challenges=challenges)


@app.route('/challenge/<challenge_id>')
def challenge_view(challenge_id):
    """View a specific challenge"""
    if challenge_id not in challenges:
        return "Challenge not found", 404

    challenge = challenges[challenge_id]
    folder = challenge['folder']

    # Read README.txt if it exists
    readme_path = os.path.join(folder, 'README.txt')
    readme_html = ""
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            raw_readme = f.read()
            # Convert Markdown to HTML
            readme_html = Markup(markdown.markdown(raw_readme))

    # List other files (excluding README and hidden files)
    file_list = [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
           and f != "README.txt"
           and not f.startswith(".")
    ]

    return render_template(
        'challenge.html',
        challenge_id=challenge_id,
        challenge=challenge,
        readme=readme_html,  # Pass rendered HTML
        files=file_list
    )


@app.route('/submit_flag/<challenge_id>', methods=['POST'])
def submit_flag(challenge_id):
    """Validate submitted flag"""
    data = request.get_json()
    submitted_flag = data.get('flag', '').strip().upper()

    if challenge_id not in challenges:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    correct_flag = xor_decode(challenges[challenge_id]['flag'], XOR_KEY).upper()

    if submitted_flag == correct_flag:
        return jsonify({"status": "correct"})
    else:
        return jsonify({"status": "incorrect"})


@app.route('/open_folder/<challenge_id>', methods=['POST'])
def open_folder(challenge_id):
    """Open the challenge folder in the file manager"""
    if challenge_id not in challenges:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    config = get_server_config()

    if config['in_docker']:
        # In Docker: Can't open host file manager, return helpful message
        return jsonify({
            "status": "info",
            "message": "Running in Docker. Use 'docker-compose exec ctf bash' to access files."
        })

    folder = challenges[challenge_id]['folder']
    try:
        # Try xdg-open first, fallback to gio open
        try:
            subprocess.Popen(['xdg-open', folder])
        except FileNotFoundError:
            subprocess.Popen(['gio', 'open', folder])
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/run_script/<challenge_id>', methods=['POST'])
def run_script(challenge_id):
    """Run the helper script in gnome-terminal"""
    if challenge_id not in challenges:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    config = get_server_config()

    # Resolve absolute paths
    folder = os.path.abspath(challenges[challenge_id]['folder'])
    script = challenges[challenge_id]['script']
    script_path = os.path.join(folder, script)

    if not os.path.exists(script_path):
        return jsonify({"status": "error", "message": "Script not found"}), 404

    try:
        if config['in_docker']:
            # In Docker: Run script directly in background, show output in logs
            result = subprocess.run(
                ['bash', script_path],
                cwd=folder,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return jsonify({
                    "status": "success",
                    "message": f"Script completed. Output: {result.stdout[:200]}..."
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": f"Script failed: {result.stderr[:200]}"
                })
        else:
            # Native: Use gnome-terminal as before
            subprocess.Popen([
                'gnome-terminal',
                '--working-directory', folder,
                '--',
                'bash', script_path
            ])
            return jsonify({"status": "success"})

    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "message": "Script timed out"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# === Add environment info endpoint ===
@app.route('/api/environment')
def environment_info():
    """Return environment information for debugging"""
    config = get_server_config()
    return jsonify({
        "in_docker": config['in_docker'],
        "host": config['host'],
        "port": config['port'],
        "debug": config['debug'],
        "python_version": os.sys.version,
        "working_directory": os.getcwd()
    })


# === Simulated Open Ports (Challenge #17) ===
FAKE_FLAGS = {
    8029: "CCRI-WAYN-1203",       # ✅ REAL FLAG
    8013: "EFTS-YHYL-2833",       # fake
    8002: "ZPEQ-7175-EDCX",       # fake
    8033: "ZYIA-5315-LUYN",       # fake
    8016: "VFHD-9579-QGRW",       # fake
}

JUNK_RESPONSES = {
    8001: "Welcome to Dev HTTP Server v1.3\nPlease login to continue.",
    8009: "🔒 Unauthorized: API key required.",
    8015: "503 Service Unavailable\nTry again later.",
    8020: "<html><body><h1>It works!</h1><p>Apache2 default page.</p></body></html>",
    8028: "DEBUG: Connection established successfully.",
    8033: "💡 Tip: Scan only the ports you really need.",
    8039: "ERROR 400: Bad request syntax.",
    8045: "System maintenance in progress. Expected downtime: 13 minutes.",
    8051: "Welcome to Experimental IoT Server (beta build).",
    8058: "Python HTTP Server: directory listing not allowed.",
    8064: "💻 Dev API v0.1 — POST requests only.",
    8077: "403 Forbidden: You don't have permission to access this resource.",
    8083: "Error 418: I'm a teapot.",
    8089: "Hello World!\nTest endpoint active.",
    8098: "Server under maintenance.\nPlease retry in 5 minutes."
}

SERVICE_NAMES = {
    8001: "dev-http",
    8004: "configd",
    8009: "secure-api",
    8015: "maintenance",
    8020: "apache",
    8023: "metricsd",
    8028: "debug-service",
    8033: "help-service",
    8039: "http",
    8045: "maintenance",
    8047: "sysmon-api",  # ✅ real flag is here, neutral name
    8051: "iot-server",
    8058: "http",
    8064: "dev-api",
    8072: "update-agent",
    8077: "secure-api",
    8083: "http",
    8089: "test-service",
    8095: "metrics-gateway",
    8098: "maintenance"
}

# === Start Real Services on Ports 8000–8100 ===
ALL_PORTS = {}
ALL_PORTS.update(FAKE_FLAGS)
ALL_PORTS.update(JUNK_RESPONSES)


class PortHandler(BaseHTTPRequestHandler):
    """Custom HTTP handler for simulated ports"""

    def do_GET(self):
        response = ALL_PORTS.get(self.server.server_port, "Connection refused")
        service_name = SERVICE_NAMES.get(self.server.server_port, "http")
        banner = f"👋 Welcome to {service_name} Service\n\n"
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.send_header("Server", service_name)  # Hint Nmap
        self.send_header("X-Service-Name", service_name)  # Custom header for Nmap
        self.end_headers()
        self.wfile.write((banner + response).encode("utf-8"))

    def log_message(self, format, *args):
        # Suppress logging
        return


def start_fake_service(port):
    """Start a lightweight HTTP server on the given port"""
    config = get_server_config()
    bind_host = '0.0.0.0' if config['in_docker'] else '127.0.0.1'

    try:
        server = HTTPServer((bind_host, port), PortHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print(f"🛰️  Simulated service running on {bind_host}:{port} ({SERVICE_NAMES.get(port, 'http')})")
    except OSError as e:
        print(f"❌ Could not bind port {port}: {e}")


# Launch all fake services
for port in ALL_PORTS.keys():
    start_fake_service(port)

# === Start Flask Hub ===
if __name__ == '__main__':
    config = get_server_config()

    print(f"🌐 Student hub running on http://{config['host']}:{config['port']}")
    if config['in_docker']:
        print(f"🔗 Access from host at: http://localhost:{config['port']}")

    app.run(
        host=config['host'],
        port=config['port'],
        debug=config['debug']
    )