#!/bin/bash
# setup_dev_env.sh - Set up CCRI STEM Day dev environment (pipx + ensurepath)

set -e

echo "🌱 Setting up CCRI STEM Day CTF developer environment..."

# --- Detect distro
DETECTED_OS=$(grep -oP '(?<=^ID=).+' /etc/os-release | tr -d '"')
DETECTED_NAME=$(grep -oP '(?<=^NAME=).+' /etc/os-release | tr -d '"')

echo "🔍 Detected OS ID: $DETECTED_OS"
echo "🔍 Detected OS Name: $DETECTED_NAME"

if grep -qi "parrot" /etc/os-release; then
    DISTRO="parrot"
elif grep -qi "mint" /etc/os-release || grep -qi "mint" /etc/lsb-release 2>/dev/null; then
    DISTRO="mint"
elif grep -qi "ubuntu" /etc/os-release; then
    DISTRO="ubuntu"
elif grep -qi "debian" /etc/os-release; then
    DISTRO="debian"
else
    echo "⚠️ Unsupported distro. Please install the following packages manually:"
    echo "  git python3 python3-pip python3-venv python3-markdown python3-scapy"
    echo "  exiftool zbar-tools steghide hashcat unzip nmap tshark pipx"
    echo "  Then run: pipx install flask"
    exit 1
fi

echo "📦 Final detected distro: $DISTRO"
sudo apt update

# --- Install system dependencies
SYSTEM_PACKAGES="git python3 python3-pip python3-venv \
python3-markdown python3-scapy \
exiftool zbar-tools steghide hashcat unzip nmap tshark pipx"

echo "📦 Installing system packages..."
sudo apt install -y $SYSTEM_PACKAGES

# --- Ensure pipx is initialized
if ! command -v pipx >/dev/null 2>&1; then
    echo "❌ pipx installation failed. Please install pipx manually and rerun this script."
    exit 1
fi

# --- Add ~/.local/bin to PATH (for pipx apps)
echo "🔧 Ensuring ~/.local/bin is on PATH..."
pipx ensurepath >/dev/null 2>&1 || true
export PATH="$HOME/.local/bin:$PATH"

# --- Install Flask using pipx
if pipx list | grep -q flask; then
    echo "✅ Flask already installed via pipx."
else
    echo "📦 Installing Flask with pipx (isolated)..."
    pipx install flask
fi

# --- Optional: Add user to Wireshark group
if groups $USER | grep -q wireshark; then
    echo "✅ User already in wireshark group."
else
    echo "🔒 Adding $USER to wireshark group (for tshark without sudo)..."
    sudo usermod -aG wireshark $USER
    echo "ℹ️ Log out and back in to apply group changes."
fi

echo "🎉 Setup complete!"
echo "✅ Flask installed via pipx and ~/.local/bin added to PATH."
echo "ℹ️ To run Flask later, use: pipx run flask <options>"
