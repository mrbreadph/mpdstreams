@echo off
echo 🎬 MPD Stream Player - Server Launcher
echo ========================================
echo.
echo Choose your server option:
echo.
echo 1. Full CORS Proxy Server (Recommended)
echo    - Solves all CORS issues
echo    - Proxies external requests
echo.
echo 2. Simple HTTP Server 
echo    - Basic server for testing
echo    - May still have some CORS issues
echo.
echo 3. Cancel
echo.
set /p choice="Enter your choice (1, 2, or 3): "

if "%choice%"=="1" goto proxy
if "%choice%"=="2" goto simple
if "%choice%"=="3" goto end

:proxy
echo.
echo Starting CORS Proxy Server...
python cors-proxy-server.py
goto end

:simple
echo.
echo Starting Simple HTTP Server...
python simple-server.py
goto end

:end
echo.
echo Server stopped. Press any key to exit...
pause >nul
