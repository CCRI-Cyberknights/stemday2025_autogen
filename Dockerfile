# Dockerfile - This defines what goes inside the container
FROM python:3.11-slim

# Install the tools your CTF challenges need
RUN apt-get update && apt-get install -y \
    git \
    exiftool \
    zbar-tools \
    steghide \
    hashcat \
    unzip \
    nmap \
    tshark \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a user (security best practice)
RUN useradd -m -s /bin/bash ctfuser
WORKDIR /home/ctfuser

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire CTF project into the container
COPY --chown=ctfuser:ctfuser . /home/ctfuser/ctf/

# Make all shell scripts executable
RUN find /home/ctfuser/ctf -name "*.sh" -exec chmod +x {} \;

# Switch to the ctf user
USER ctfuser

# Expose the port Flask will run on
EXPOSE 5000

# Smart server.py detection - tries student version first, falls back to admin version
CMD ["bash", "-c", "if [ -f /home/ctfuser/ctf/web_version/server.py ]; then python /home/ctfuser/ctf/web_version/server.py; elif [ -f /home/ctfuser/ctf/web_version_admin/server.py ]; then cd /home/ctfuser/ctf/web_version_admin && python server.py; else echo 'No server.py found' && find /home/ctfuser/ctf -name '*.py' -type f; fi"]