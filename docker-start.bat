@echo off
echo Starting CCRI CTF with Docker...
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed!
    echo.
    echo INSTALL DOCKER DESKTOP:
    echo 1. Go to: https://docs.docker.com/desktop/install/windows-install/
    echo 2. Download Docker Desktop for Windows
    echo 3. Run the installer and restart your computer
    echo 4. Start Docker Desktop from the Start menu
    echo 5. Wait for the whale icon to appear in your system tray
    echo 6. Run this script again
    echo.
    pause
    exit /b 1
)

REM Check if Docker is running
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is installed but not running!
    echo.
    echo START DOCKER DESKTOP:
    echo 1. Press Windows key and search for "Docker Desktop"
    echo 2. Click on Docker Desktop to start it
    echo 3. Wait for the whale icon in your system tray to stop animating
    echo 4. The whale icon should be solid when ready
    echo 5. This may take 1-2 minutes on first startup
    echo 6. Run this script again when Docker is ready
    echo.
    echo TIP: You can also check if Docker is ready by running: docker ps
    echo.
    pause
    exit /b 1
)

echo SUCCESS: Docker is running
echo.

REM Build the web version first
echo Building web version...
cd web_version_admin\create_website
call build_web_version.sh
cd ..\..

REM Start with Docker Compose
echo Starting Docker containers...
docker-compose up --build -d

if %errorlevel% neq 0 (
    echo ERROR: Failed to start containers
    echo.
    echo TROUBLESHOOTING:
    echo - Make sure no other programs are using port 5000
    echo - Try running: docker-compose down
    echo - Then run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo SUCCESS: CTF is starting up!
echo INFO: Building containers for the first time may take 5-10 minutes
echo INFO: It will be available at: http://localhost:5000
echo INFO: Wait about 30 seconds after build completes...
echo.

REM Wait a bit for services to start
echo Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Open browser automatically
start http://localhost:5000

echo.
echo MANAGEMENT COMMANDS:
echo - To stop the CTF: docker-compose down
echo - To see logs: docker-compose logs -f
echo - To rebuild: docker-compose up --build
echo - To check status: docker-compose ps
echo.
echo The CTF should now be opening in your browser
echo.
pause