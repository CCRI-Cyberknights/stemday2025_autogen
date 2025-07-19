#!/bin/bash
# 🌟 CCRI CyberKnights Contributor Setup Script
set -e

echo
echo "🚀 Setting up your STEMDay_2025 contributor environment..."
echo "============================================================"
echo

# --- Update package list and install dependencies ---
echo "📦 Installing system dependencies..."
sudo apt update

sudo apt install -y \
  git \
  python3 python3-pip python3-venv \
  python3-markdown python3-scapy \
  exiftool zbar-tools steghide hashcat unzip nmap tshark qrencode \
  xdg-utils lsof vim-common util-linux

# --- Upgrade pip and install Python packages ---
echo
echo "🐍 Installing Python packages..."
python3 -m pip install --upgrade pip
python3 -m pip install flask

# --- Configure Git (if not already configured) ---
if ! git config user.name >/dev/null 2>&1; then
    echo
    echo "🔧 Configuring Git for the first time..."
    read -rp "Enter your Git name: " git_name
    read -rp "Enter your Git email: " git_email
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
    git config --global credential.helper store
    echo "✅ Git configuration saved."
else
    echo
    echo "✅ Git is already configured:"
    echo "   Name : $(git config user.name)"
    echo "   Email: $(git config user.email)"
fi
echo
echo "🎉 Setup complete! You are now ready to clone the repo!"
