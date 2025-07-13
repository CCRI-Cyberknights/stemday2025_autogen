#!/bin/bash
# setup_dev_env.sh - Set up CCRI STEM Day dev environment (Parrot system Flask, others pipx)

set -e

echo "🌱 Setting up CCRI STEM Day CTF developer environment..."

# --- Detect distro (Debian family only for now)
DETECTED_OS=$(grep -oP '(?<=^ID=).+' /etc/os-release | tr -d '"')
echo "🔍 Detected OS: $DETECTED_OS"

if [[ "$DETECTED_OS" =~ (parrot|mint|ubuntu|debian) ]]; then
    echo "📦 Supported distro: $DETECTED_OS"
else
    echo "⚠️ Unsupported distro. Please install these manually:"
    echo "  git python3 python3-pip python3-venv python3-markdown python3-scapy"
    echo "  exiftool zbar-tools steghide hashcat unzip nmap tshark pipx"
    echo "  Then run: pipx install flask && pipx inject flask markdown markupsafe"
    exit 1
fi

sudo apt update

# --- Install system dependencies (common)
SYSTEM_PACKAGES="git python3 python3-pip python3-venv \
python3-markdown python3-scapy \
exiftool zbar-tools steghide hashcat unzip nmap tshark pipx"
echo "📦 Installing system packages..."
sudo apt install -y $SYSTEM_PACKAGES

# --- Install Flask
if [[ "$DETECTED_OS" == "parrot" ]]; then
    echo "📦 Parrot OS detected. Installing system Flask via apt..."
    sudo apt install -y python3-flask
else
    echo "📦 Installing Flask in an isolated pipx environment..."
    if command -v pipx >/dev/null 2>&1; then
        pipx ensurepath >/dev/null 2>&1 || true
        export PATH="$HOME/.local/bin:$PATH"

        if pipx list | grep -q flask; then
            echo "✅ Flask already installed via pipx."
        else
            echo "📦 Installing latest Flask (3.x) with pipx..."
            pipx install flask
        fi

        echo "📦 Injecting required Python packages (markdown, markupsafe)..."
        pipx inject flask markdown markupsafe

    else
        echo "⚠️ pipx not found. Installing Flask system-wide with pip (not recommended)..."
        sudo python3 -m pip install flask markdown markupsafe
    fi
fi

echo "🎉 Setup complete!"
echo "✅ Flask installed and ~/.local/bin added to PATH (if needed)."
echo "ℹ️ To run Flask later, use: python3 -m flask or pipx run flask <options>"
