# Changelog

All notable changes to the CCRI STEM Day CTF project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Docker containerization support for cross-platform compatibility
- Environment auto-detection (Docker vs native execution)
- Docker Compose configuration for easy deployment
- Smart server.py that adapts behavior based on runtime environment
- Cross-platform launcher script (`docker-start.sh`) for Linux/macOS
- Windows batch script (`docker-start.bat`) with comprehensive Docker setup guidance
- PowerShell alternative script (`start-ctf.ps1`) for Windows users
- Python requirements.txt for dependency management
- pyproject.toml for modern Python project configuration and packaging
- Environment information API endpoint (`/api/environment`)
- Improved error handling and user feedback in web interface
- Docker-aware script execution (shows output in browser when in container)
- Enhanced README with comprehensive setup instructions for both Docker and native modes
- Comprehensive CHANGELOG.md following Keep a Changelog format
- Semantic versioning implementation across project files
- PyCharm run configuration support for both Windows and Linux development

### Changed
- Server binding: automatically uses `0.0.0.0` in Docker, `127.0.0.1` in native mode
- Script execution: runs directly in Docker containers, opens terminal in native mode
- Folder access: shows helpful Docker messages instead of trying to open host file manager
- Updated build process to work consistently across different environments
- Enhanced web interface with environment-specific help messages
- Improved path resolution in build scripts for better portability
- Project structure: added modern Python packaging with pyproject.toml
- Documentation: comprehensive README and CHANGELOG following industry standards
- Dockerfile: now uses pyproject.toml instead of requirements.txt for dependency management
- Launcher scripts: Windows-specific implementations with detailed setup instructions

### Fixed
- Cross-platform compatibility issues between different Linux distributions
- Flask version compatibility (supports both 2.x and 3.x)
- Path handling issues in build scripts
- Permission detection and handling in Docker startup script
- Environment variable handling for different deployment scenarios

### Security
- Container isolation for challenge execution
- Localhost-only binding in native mode for better security
- Read-only challenge file mounting in Docker containers
- Version tracking and dependency management for security updates

## [1.0.0] - Initial Release

### Added
- 18 CTF challenges covering multiple cybersecurity domains:
  - **Steganography**: Hidden data extraction from images
  - **Cryptography**: Base64, ROT13, Vigenère cipher challenges
  - **Forensics**: Metadata analysis, log investigation, binary inspection
  - **Networking**: Packet capture analysis, port scanning, subdomain enumeration
  - **System Analysis**: Process inspection, hash cracking, archive password cracking
- Web-based CTF hub with Flask backend
- Challenge management system with XOR-encoded flags
- Automatic challenge script execution
- File manager integration for challenge exploration
- Progress tracking with localStorage
- Responsive grid-based challenge interface
- Markdown support for challenge descriptions
- Simulated vulnerable services for network scanning challenges

### Features
- **Admin Tools**:
  - Flag encoding/decoding system
  - Student version builder
  - Challenge metadata management
  - Automated script permission setting
- **Student Experience**:
  - Browser-based challenge interface
  - Interactive helper scripts
  - Real-time flag validation
  - Progress persistence
  - File download capabilities
- **Challenge Categories**:
  - Steganography (steghide extraction)
  - Encoding/Decoding (Base64, ROT13)
  - Cryptanalysis (Vigenère cipher breaking)
  - Password Cracking (ZIP archives, hashcat)
  - Binary Analysis (hex dumps, executable inspection)
  - Network Forensics (pcap analysis, nmap scanning)
  - System Forensics (log analysis, metadata extraction)
  - OSINT (subdomain enumeration, HTTP headers)

### Technical Details
- **Backend**: Python Flask with auto-reload capability
- **Frontend**: Vanilla JavaScript with responsive CSS
- **Security**: XOR flag encryption with server-side decryption
- **Compatibility**: Debian-based Linux distributions (Ubuntu, Mint, Parrot)
- **Dependencies**: Automated installation of security tools (nmap, hashcat, wireshark, etc.)
- **Architecture**: Modular challenge structure with standardized helper scripts

### Installation
- Native setup script for Debian-based systems
- Automated dependency installation
- Desktop launcher integration
- Web server management scripts (start/stop)

---

## Version History Summary

- **v1.0.0**: Initial CTF platform with 18 challenges and native Linux support
- **v2.0.0** (Unreleased): Added Docker support, cross-platform compatibility, and environment auto-detection

---

## Contributing

When adding entries to this changelog:

1. **Keep entries in chronological order** (newest first)
2. **Use semantic versioning** for releases (update `pyproject.toml` version accordingly)
3. **Categorize changes** using:
   - `Added` for new features
   - `Changed` for changes in existing functionality
   - `Deprecated` for soon-to-be removed features
   - `Removed` for now removed features
   - `Fixed` for any bug fixes
   - `Security` for vulnerability fixes
4. **Include relevant details** like affected components or breaking changes
5. **Link to issues/PRs** when applicable
6. **Date releases** when they are published
7. **Update version** in `pyproject.toml` when creating releases

## Support

For questions about changes or version compatibility:
- Check the README.md for current setup instructions
- Review the CONTRIBUTING.md for development guidelines
- Contact CCRI CyberKnights club members for technical support