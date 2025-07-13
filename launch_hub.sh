#!/bin/bash
# launch_hub.sh - dynamic launcher for CCRI CTF

# Resolve directory this script is in
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Call start_web_hub.sh relative to this location
"$SCRIPT_DIR/stemday2025/web_version/start_web_hub.sh"
