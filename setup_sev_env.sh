#!/bin/bash
# setup_dev_env.sh - Auto-detect distro and install CCRI STEM Day dependencies

set -e

echo "🌱 Setting up developer environment for CCRI STEM Day CTF..."

# --- Detect distro
if grep -qi parrot /etc/os-release; then
    DISTRO="parrot"
elif grep -qi mint /etc/os-release; then
    DISTRO="mint"
elif grep -qi ubuntu /etc/os-release; then
    DISTRO="ubuntu"
elif grep -qi debian /etc/os-release; then
    DISTRO="debian"
else
    echo "⚠️ Unsupported distro. This script supports Parrot, Debian, Ubuntu, and Linux Mint."
    echo "You can install the following packages manually on your system:"
    echo "  git python3 python3-pip python3-venv python3-markdown python3-scapy"
    echo "  exiftool zbar-tools steghide hashcat unzip nmap tshark"
    exit 1
fi

echo "📦 Detected distro: $DISTRO"
sudo apt update

COMMON_PACKAGES="git python3 python3-pip python3-venv \
python3-markdown python3-scapy exiftool zbar-tools steghide \
hashcat unzip nmap tshark"

EXTRA_PACKAGES=""

if [ "$DISTRO" = "parrot" ]; then
    echo "✅ Parrot OS detected. Installing minimal missing tools..."
elif [ "$DISTRO" = "mint" ] || [ "$DISTRO" = "debian" ] || [ "$DISTRO" = "ubuntu" ]; then
    echo "✅ Debian/Ubuntu-based system detected. Adding developer extras..."
    EXTRA_PACKAGES="build-essential libzbar0 libimage-exiftool-perl"
fi

sudo apt install -y $COMMON_PACKAGES $EXTRA_PACKAGES

# --- Optional: Wireshark group setup
if groups $USER | grep -q wireshark; then
    echo "✅ User already in wireshark group."
else
    echo "🔒 Adding $USER to wireshark group (for tshark without sudo)..."
    sudo usermod -aG wireshark $USER
    echo "ℹ️ Log out and back in to apply group changes."
fi

echo "🎉 Setup complete! You’re ready to clone and work on the repo."
