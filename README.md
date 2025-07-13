### PyCharm Integration

**Windows Run Configuration:**
```
Name: Start CTF (Docker)
Execute: Script file ✓
Script path: C:\Users\user\PycharmProjects\stemday2025\docker-start.bat
Working directory: C:\Users\user\PycharmProjects\stemday2025
Interpreter: cmd.exe
Interpreter options: /c
☑ Execute in the terminal
```

**Linux/macOS Run Configuration:**
```
Name: Start CTF (Docker)  
Execute: Script file ✓
Script path: /path/to/stemday2025/docker-start.sh
Working directory: /path/to/stemday2025
Interpreter: /bin/bash
☑ Execute in the terminal
```# 🌟 `stemday2025` Project README

Welcome to the **CCRI CyberKnights STEM Day VM Project!** 🎉  
This repository powers a custom **Capture The Flag (CTF)** experience designed for high school students, featuring both **Docker** and **native** deployment options for maximum compatibility across different environments.

👥 **This repo is for CCRI CyberKnights club members only.**  
It contains all the source files, admin tools, and scripts used to **build and maintain** the student-facing version of the CTF.

## 🚀 Quick Start

**Option 1: Docker (Recommended - Works Everywhere)**

*Windows:*
```bash
git clone <your-repo-url>
cd stemday2025
.\docker-start.bat
```

*Linux/macOS:*
```bash
git clone <your-repo-url>
cd stemday2025
./docker-start.sh
```

**Option 2: Native Setup (Linux Only)**
```bash
git clone <your-repo-url>
cd stemday2025
./1_setup_dev_env.sh
./2_start_web_hub.sh
```

---

## 🗂️ Project Structure

```
stemday2025/
├── README.md                      # This file
├── CONTRIBUTING.md                # Collaboration guide for club members
│
├── 🐳 DOCKER FILES (NEW!)
├── Dockerfile                     # Container definition
├── docker-compose.yml             # Easy container management
├── requirements.txt               # Python dependencies
├── docker-start.sh                # Simple Docker startup script
│
├── 📜 SETUP SCRIPTS
├── 1_setup_dev_env.sh             # Install dependencies natively (Linux)
├── 2_start_web_hub.sh             # Start Flask server natively (Linux)  
├── 3_stop_web_hub.sh              # Stop Flask server (Linux)
├── docker-start.sh                # Docker startup script (Linux/macOS)
├── docker-start.bat               # Docker startup script (Windows)
├── start-ctf.ps1                  # PowerShell alternative (Windows)
│
├── 🎯 CHALLENGE CONTENT
├── challenges/                    # Interactive CTF challenges (source)
├── web_version/                   # Student-facing web portal (auto-generated)
├── web_version_admin/             # Admin-only tools and templates
│   ├── challenges.json            # Challenge definitions with flags
│   ├── server.py                  # Flask server (environment-aware)
│   ├── templates/                 # HTML templates
│   ├── static/                    # CSS and assets
│   └── create_website/
│       └── build_web_version.sh   # Build student portal
│
└── Launch CCRI CTF Hub.desktop    # Desktop shortcut
```

In the **student distribution**, only essential files are included:
```
Desktop/
├── CCRI_CTF/                     # Student bundle (built from this repo)
│   ├── challenges/               # Interactive CTF challenges
│   ├── web_version/              # Student-facing web portal (ready-to-use)
│   ├── docker-start.sh           # Docker launcher
│   ├── Launch CCRI CTF Hub.desktop # Desktop shortcut
└── (no admin tools or source flags)
```

---

## 🐳 Docker Setup (Recommended)

### Prerequisites
- **Docker Desktop** installed and running
  - **Windows:** [Download Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)
  - **macOS:** [Download Docker Desktop](https://docs.docker.com/desktop/install/mac-install/)
  - **Linux:** `sudo apt install docker.io docker-compose` or [Docker Desktop](https://docs.docker.com/desktop/install/linux-install/)

### Quick Start

**Windows:**
```bash
# 1. Clone and enter project
git clone <your-repo-url>
cd stemday2025

# 2. Start with Docker (includes Docker installation help)
.\docker-start.bat

# 3. Access at http://localhost:5000
```

**Linux/macOS:**
```bash
# 1. Clone and enter project  
git clone <your-repo-url>
cd stemday2025

# 2. Start with Docker (builds automatically)
chmod +x docker-start.sh
./docker-start.sh

# 3. Access at http://localhost:5000
```

### Docker Commands

**Windows (using .bat script):**
```batch
# Start CTF with guided setup
.\docker-start.bat

# Or use Docker Compose directly
docker-compose up --build -d
docker-compose down
```

**Linux/macOS (using shell script):**
```bash
# Start CTF
./docker-start.sh

# Manual Docker commands
docker-compose up --build -d
docker-compose logs -f
docker-compose down
```

**Universal Docker Commands:**
```bash
# View logs
docker-compose logs -f

# Stop CTF  
docker-compose down

# Get shell inside container
docker-compose exec ctf bash

# Rebuild after changes
docker-compose up --build
```

### Why Docker?
✅ **Consistent environment** across all operating systems  
✅ **No package conflicts** - everything runs in isolation  
✅ **Easy setup** - students just need Docker installed  
✅ **Automatic dependency management**  
✅ **Works on Windows, Mac, Linux** identically  

---

## 💻 Native Setup (Traditional)

### Prerequisites
- **Linux distributions:** Ubuntu, Debian, Mint, or Parrot
- **Python 3.x** and **pip**
- **Various CTF tools** (automatically installed by setup script)

### Setup Process
```bash
# 1. Clone repository
git clone <your-repo-url>
cd stemday2025

# 2. Run setup (installs dependencies)
chmod +x 1_setup_dev_env.sh
./1_setup_dev_env.sh

# 3. Start the hub
./2_start_web_hub.sh

# 4. Access at http://localhost:5000
```

### Native Dependencies
The setup script automatically installs:
- **Python packages:** Flask, MarkupSafe, Markdown
- **CTF tools:** exiftool, zbar-tools, steghide, hashcat, unzip, nmap, tshark
- **System tools:** git, python3-venv, pipx

---

## 🛠 Admin Workflow

### Building the Student Web Portal
```bash
cd web_version_admin/create_website
./build_web_version.sh
```

This script:
- Encodes admin flags using XOR encryption
- Copies challenge files and web assets
- Generates the student-ready `web_version/` folder
- Makes all helper scripts executable

### Environment-Aware Server
The `server.py` automatically detects its environment:

**🐳 Docker Mode:**
- Binds to `0.0.0.0:5000` (accessible from host)
- Runs scripts directly and shows output in browser
- Shows Docker-specific help messages

**💻 Native Mode:**
- Binds to `127.0.0.1:5000` (localhost only, more secure)
- Opens terminal windows for script execution
- Opens file manager for folder access

### Testing Both Environments
```bash
# Test native mode
cd web_version
python server.py

# Test Docker mode
docker-compose up --build
```

### Debugging
- **Environment info:** Visit `http://localhost:5000/api/environment`
- **Docker logs:** `docker-compose logs -f`
- **Native logs:** Check terminal output

---

## 🎓 Student Instructions

### For Students Using Docker

**Windows Students:**
```bash
# 1. Install Docker Desktop from https://docs.docker.com/desktop/install/windows-install/

# 2. Get CTF files
git clone [provided-url]
cd stemday2025

# 3. Start CTF (includes setup help)
.\docker-start.bat

# 4. Open http://localhost:5000 in browser
```

**Linux/macOS Students:**
```bash
# 1. Install Docker (Linux: sudo apt install docker.io docker-compose)
# 2. Get CTF files
git clone [provided-url]
cd stemday2025

# 3. Start CTF
./docker-start.sh

# 4. Open http://localhost:5000 in browser
```

### For Students Using Native Setup
```bash
# 1. Get CTF files (Linux required)
git clone [provided-url]
cd stemday2025

# 2. Run setup
./1_setup_dev_env.sh

# 3. Start CTF
./2_start_web_hub.sh

# 4. Open http://localhost:5000 in browser
```

---

## 🔧 Development

### File Structure for Developers
- **`challenges/`** - Individual CTF challenges with README.txt files
- **`web_version_admin/challenges.json`** - Challenge metadata and flags (admin only)
- **`web_version_admin/server.py`** - Smart Flask server with environment detection
- **`web_version_admin/templates/`** - Jinja2 HTML templates
- **`web_version_admin/static/`** - CSS, JavaScript, and static assets

### Adding New Challenges
1. Create folder in `challenges/`
2. Add challenge files and `README.txt`
3. Create helper script (e.g., `solve.sh`)
4. Update `web_version_admin/challenges.json`
5. Run `build_web_version.sh` to generate student version

### Flag Format
All flags follow the pattern: `CCRI-XXXX-####`
- Stored encrypted in admin `challenges.json`
- Automatically decrypted by the web server
- Validated case-insensitively

### Environment Variables
```bash
# Force Docker mode detection
export DOCKER_CONTAINER=true

# Change server port
export FLASK_PORT=8080

# Enable debug mode (native only)
export FLASK_DEBUG=true
```

---

## 🛡️ Security Features

**🔒 Flag Protection:**
- Admin flags are XOR-encoded in student version
- Decryption happens server-side only
- Students never see plaintext flags in files

**🌐 Network Security:**
- Docker mode: Binds to all interfaces (required for container access)
- Native mode: Binds to localhost only (more secure)
- Simulated vulnerable services run on isolated ports

**📁 File Access:**
- Challenge files are read-only in Docker
- Script execution is sandboxed
- No admin tools included in student distribution

---

## 🌍 Cross-Platform Compatibility

| Platform | Docker Support | Native Support | Recommended |
|----------|----------------|----------------|-------------|
| **Linux (Ubuntu/Debian)** | ✅ Full | ✅ Full | Either |
| **Linux (Other)** | ✅ Full | ⚠️ Manual setup | Docker |
| **Windows** | ✅ Full | ❌ Not supported | Docker |
| **macOS** | ✅ Full | ⚠️ Limited tools | Docker |

---

## 🙌 Club Member Guidelines

✅ **Keep admin-only flags and tools** out of `web_version/`  
✅ **Test both Docker and native modes** before release  
✅ **Use relative paths** for portability  
✅ **Don't commit** `.pyc` files or student-only builds  
✅ **Update this README** when adding new features  
✅ **Test on multiple platforms** when possible  

---

## 📊 Challenge Categories

The CTF includes these challenge types:
- **🔐 Cryptography:** Base64, ROT13, Vigenère ciphers
- **🖼️ Steganography:** Hidden data in images and files
- **🔨 Forensics:** Metadata analysis, log investigation
- **💻 Binary Analysis:** Hex dumps, executable inspection
- **🌐 Networking:** Packet capture analysis, port scanning
- **🕵️ OSINT:** Subdomain enumeration, HTTP headers

---

## 🚨 Troubleshooting

### Docker Issues

**Windows:**
```batch
# Permission denied or "Docker not running"
# 1. Start Docker Desktop from Start menu
# 2. Wait for whale icon in system tray to be solid (not spinning)
# 3. Run: .\docker-start.bat

# Port already in use
docker-compose down
# Check what's using port 5000:
netstat -ano | findstr :5000
```

**Linux/macOS:**
```bash
# Permission denied
sudo usermod -aG docker $USER
newgrp docker

# Port already in use
docker-compose down
sudo lsof -ti:5000 | xargs kill -9

# Container won't start
docker-compose logs ctf
```

### Native Issues
```bash
# Flask import errors
pip install flask markupsafe markdown

# Permission denied on scripts
chmod +x *.sh

# Port 5000 busy
pkill -f "flask run"
```

### General Issues
- **Can't access localhost:5000:** Check firewall settings
- **Scripts don't work:** Ensure proper file permissions
- **Challenges missing:** Run `build_web_version.sh`

---

## 📞 Support

For technical issues or contributions:
1. Check this README and troubleshooting section
2. See `CONTRIBUTING.md` for development guidelines
3. Contact CCRI CyberKnights club members
4. Create an issue in the repository (club members only)

---

## 🎓 Thanks for helping build CCRI CyberKnights STEM Day CTF!

This project makes cybersecurity education accessible to high school students through hands-on, practical challenges. Whether you're running it in Docker for consistency or natively for performance, you're helping students learn valuable security skills!

**🐳 Docker = Simplicity & Compatibility**  
**💻 Native = Performance & Full Features**  
**🎯 Both = Maximum Reach & Impact**