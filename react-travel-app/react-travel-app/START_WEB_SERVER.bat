@echo off
echo ===================================
echo   Vietnam UrbanQuest - Web Server
echo ===================================
echo.
echo Starting Backend API Server...
cd backend
start "Backend API" cmd /k "python main.py"
cd ..
timeout /t 3 /nobreak > nul

echo.
echo Starting Frontend Web Server...
echo.
echo Open your browser and go to:
echo   http://localhost:8080
echo.
echo Pages available:
echo   - Home: http://localhost:8080/index.html
echo   - Login: http://localhost:8080/login.html
echo   - Signup: http://localhost:8080/signup.html
echo   - About Us: http://localhost:8080/about-us.html
echo   - Information: http://localhost:8080/information.html
echo.
echo Press Ctrl+C to stop the servers
echo.
python -m http.server 8080
