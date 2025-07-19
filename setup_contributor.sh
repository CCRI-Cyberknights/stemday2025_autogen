#!/bin/bash
# 🌟 CCRI CyberKnights Contributor Setup Script
set -e

echo "🚀 Setting up your STEMDay_2025 contributor environment..."

# Update package list and install dependencies
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv python3-markdown python3-scapy exiftool zbar-tools steghide hashcat unzip nmap tshark qrencode

# Configure Git (if not already configured)
if ! git config user.name >/dev/null; then
    echo "🔧 Configuring Git..."
    read -rp "Enter your Git name: " git_name
    read -rp "Enter your Git email: " git_email
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
    git config --global credential.helper store
else
    echo "✅ Git already configured."
fi

# Clone the repo if not already present
if [ ! -d "stemday_2025" ]; then
    echo "📥 Cloning STEMDay_2025 repo..."
    git clone https://github.com/CCRI-Cyberknights/stemday_2025.git
else
    echo "📂 Repo already exists in $(pwd)/stemday_2025"
fi

echo "🎉 Done! Your contributor environment is ready."
