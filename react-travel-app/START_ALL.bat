@echo off
echo ===============================================
echo   Vietnam Travel App - Full Stack Startup
echo ===============================================
echo.

echo [1/2] Starting Backend Server (Port 8000)...
echo.
start "Backend Server" cmd /k "cd /d %~dp0backend && python main.py"

timeout /t 3 /nobreak > nul

echo [2/2] Starting Frontend Server (Port 3000)...
echo.
start "Frontend Server" cmd /k "cd /d %~dp0 && python -m http.server 3000"

timeout /t 2 /nobreak > nul

echo.
echo ===============================================
echo   Servers Started Successfully!
echo ===============================================
echo.
echo Backend API: http://localhost:8000
echo Frontend Web: http://localhost:3000
echo.
echo Open in browser:
echo   - Main App: http://localhost:3000/index.html
echo   - Album: http://localhost:3000/album.html
echo   - Debug: http://localhost:3000/album_debug.html
echo.
echo Press any key to open browser...
pause > nul

start http://localhost:3000/

echo.
echo Servers are running...
echo Close this window to stop all servers.
echo ===============================================
pause
