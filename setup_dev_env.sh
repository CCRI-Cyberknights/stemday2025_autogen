#!/bin/bash
# setup_dev_env.sh - Auto-detect distro and install CCRI STEM Day dependencies

set -e

echo "🌱 Setting up developer environment for CCRI STEM Day CTF (pipx version)..."

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
    echo "⚠️ Unsupported distro. This script supports Parrot, Debian, Ubuntu, and Linux Mint."
    echo "You can install the following packages manually on your system:"
    echo "  git python3 python3-pip python3-venv python3-markdown python3-scapy flask"
    echo "  exiftool zbar-tools steghide hashcat unzip nmap tshark"
    exit 1
fi

echo "📦 Final detected distro: $DISTRO"
sudo apt update

# --- Base system packages (removed flask here!)
COMMON_PACKAGES="git python3 python3-pip python3-venv \
python3-markdown python3-scapy \
exiftool zbar-tools steghide hashcat unzip nmap tshark pipx"

EXTRA_PACKAGES=""

if [ "$DISTRO" = "parrot" ]; then
    echo "✅ Parrot OS detected. Installing minimal missing tools..."
elif [ "$DISTRO" = "mint" ] || [ "$DISTRO" = "debian" ] || [ "$DISTRO" = "ubuntu" ]; then
    echo "✅ Debian/Ubuntu-based system detected. Adding developer extras..."
    EXTRA_PACKAGES="build-essential libzbar0 libimage-exiftool-perl"
fi

# Install base dependencies including pipx
sudo apt install -y $COMMON_PACKAGES $EXTRA_PACKAGES

# Ensure pipx is initialized
if ! command -v pipx >/dev/null 2>&1; then
    echo "❌ pipx installation failed. Please install pipx manually and rerun this script."
    exit 1
fi

# Install Flask using pipx
if pipx list | grep -q flask; then
    echo "✅ Flask already installed via pipx."
else
    echo "📦 Installing Flask with pipx..."
    pipx install flask
fi

# --- Optional: Wireshark group setup
if groups $USER | grep -q wireshark; then
    echo "✅ User already in wireshark group."
else
    echo "🔒 Adding $USER to wireshark group (for tshark without sudo)..."
    sudo usermod -aG wireshark $USER
    echo "ℹ️ Log out and back in to apply group changes."
fi

echo "🎉 Setup complete! Flask installed via pipx for isolation."
echo "ℹ️ To run Flask, use: pipx run flask <options>"
