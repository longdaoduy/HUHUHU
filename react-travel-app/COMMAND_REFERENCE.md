# 🔧 Quick Command Reference - Vietnam UrbanQuest Authentication

## 📋 Table of Contents
1. [Installation](#installation)
2. [Running](#running)
3. [Testing](#testing)
4. [Development](#development)
5. [Production](#production)

---

## Installation

### Backend Setup
```bash
# Navigate to backend
cd backend

# Install all dependencies
pip install -r requirements.txt

# Verify PyJWT is installed
pip show PyJWT

# Or install specific package
pip install PyJWT==2.8.1
```

### Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies (if first time)
npm install

# Or update packages
npm update
```

---

## Running

### Start Backend Server
```bash
# From backend directory
python main.py

# Server will run on http://localhost:8000
# API Docs available at http://localhost:8000/docs

# Alternative: Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend
```bash
# From frontend directory
npm start

# App will open at http://localhost:3000

# Or build for production
npm run build

# Or run on specific port
PORT=3001 npm start
```

### Start Both (Development)
```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd frontend
npm start

# Access at http://localhost:3000
```

---

## Testing

### Test with Script
```bash
# From project root
cd backend
python test_api.py

# Expected output:
# === Testing Register ===
# Status: 200
# === Testing Login ===
# Status: 200
# === Testing Get Profile ===
# Status: 200
# === Testing Logout ===
# Status: 200
```

### Test with cURL

#### Register
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "fullname": "Test User",
    "email": "test@example.com",
    "password": "Test123456",
    "phone": "0123456789"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123456"
  }'

# Response will include token:
# "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Get Profile (with token)
```bash
# Replace TOKEN with actual token from login
curl -X GET http://localhost:8000/api/user/profile \
  -H "Authorization: Bearer TOKEN"
```

#### Logout
```bash
curl -X POST http://localhost:8000/api/logout \
  -H "Authorization: Bearer TOKEN"
```

### Test with Postman

1. Import API from `http://localhost:8000/openapi.json`
2. Or manually create requests
3. Set Authorization header: `Bearer <token>`

### Test with API Docs
```
1. Open http://localhost:8000/docs
2. Try each endpoint directly in Swagger UI
3. Enter test data
4. Execute requests
```

---

## Development

### Common Development Tasks

#### Update Dependencies
```bash
cd backend
pip install --upgrade -r requirements.txt

cd ../frontend
npm update
```

#### Check Python Version
```bash
python --version
# Should be 3.8 or higher
```

#### Check Node Version
```bash
node --version
npm --version
# Node should be 14+, npm should be 6+
```

#### Run Backend with Debug Output
```bash
cd backend
python -u main.py  # -u for unbuffered output
```

#### Run Frontend with Debug
```bash
cd frontend
npm start -- --verbose
```

### Debugging

#### Backend Logs
```bash
# Check terminal output for errors
# Check function trace when endpoint fails

# Add debug prints to main.py
print(f"Debug: {variable}")
```

#### Frontend Logs
```bash
# Open browser DevTools (F12)
# Console tab shows all errors
# Network tab shows API requests

# Add console logs
console.log('Debug:', data);
```

#### Check Running Processes
```bash
# Windows (PowerShell)
Get-Process python
Get-Process node

# Linux/Mac
ps aux | grep python
ps aux | grep node
```

#### Kill Process on Port
```bash
# Windows (PowerShell) - Port 8000
$p = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($p) { Stop-Process -Id $p.OwningProcess -Force }

# Linux/Mac - Port 8000
lsof -ti:8000 | xargs kill -9

# Port 3000
lsof -ti:3000 | xargs kill -9
```

---

## Production

### Build for Production

#### Backend
```bash
# No build needed for FastAPI
# Just ensure dependencies are installed

pip install -r requirements.txt

# Run with production server
gunicorn main:app -w 4 -b 0.0.0.0:8000
```

#### Frontend
```bash
cd frontend

# Create production build
npm run build

# Build directory contains static files
# Upload to web server or CDN

# Or use production server
npm install -g serve
serve -s build -l 3000
```

### Environment Variables

#### Backend (.env)
```bash
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/db
OPENAI_API_KEY=your-openai-key
ENVIRONMENT=production
```

#### Frontend (.env)
```bash
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENV=production
```

### Docker Setup

#### Dockerfile (Backend)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

#### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=your-key
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
```

### Run with Docker
```bash
# Build images
docker-compose build

# Run containers
docker-compose up

# Stop containers
docker-compose down
```

---

## Cleanup

### Reset Development Data
```bash
# Remove user data
cd backend
rm Users.json Users_album.json

# Start fresh
python main.py
```

### Clean Node Modules
```bash
cd frontend
rm -r node_modules
npm install
```

### Clean Python Cache
```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete
```

### Full Reset
```bash
# Backend
cd backend
rm Users.json Users_album.json database.json
pip install --force-reinstall -r requirements.txt

# Frontend
cd ../frontend
rm -r node_modules build
npm install

# Start fresh
# Terminal 1: python main.py
# Terminal 2: npm start
```

---

## Verification Commands

```bash
# Check backend running
curl http://localhost:8000

# Check API docs
curl http://localhost:8000/docs

# Check frontend
curl http://localhost:3000

# List files in backend
dir backend

# List files in frontend/src
dir frontend/src

# Check Python packages
pip list | grep -i jwt

# Check npm packages
npm list --depth=0
```

---

## Performance Commands

### Backend Performance
```bash
# Monitor server with htop (Linux/Mac)
htop

# Monitor Python memory
python -m memory_profiler main.py
```

### Frontend Performance
```bash
# Check bundle size
npm run build
npm install -g serve
npx webpack-bundle-analyzer build/static/js/*.js

# Audit npm packages
npm audit

# Update audit
npm audit fix
```

---

## Database Commands

### View Users Data
```bash
# Windows PowerShell
Get-Content backend/Users.json | ConvertFrom-Json | ConvertTo-Json

# Linux/Mac
cat backend/Users.json | python -m json.tool

# Pretty print
python -c "import json; print(json.dumps(json.load(open('backend/Users.json')), indent=2, ensure_ascii=False))"
```

### Backup Data
```bash
# Windows
copy backend\Users.json backend\Users.json.backup
copy backend\Users_album.json backend\Users_album.json.backup

# Linux/Mac
cp backend/Users.json backend/Users.json.backup
cp backend/Users_album.json backend/Users_album.json.backup
```

### Clear Data
```bash
# Windows
del backend\Users.json
del backend\Users_album.json

# Linux/Mac
rm backend/Users.json
rm backend/Users_album.json
```

---

## Help Commands

### Get Help
```bash
# Python
python -help
python -m pip help

# npm
npm help
npm list --help

# FastAPI
python -c "import fastapi; help(fastapi)"
```

### View Installed Versions
```bash
python --version
pip show PyJWT
npm --version
node --version
npm list react
```

---

## Common Issues & Quick Fixes

```bash
# Issue: "Address already in use"
# Fix: Kill process on port
# Port 8000: lsof -ti:8000 | xargs kill -9
# Port 3000: lsof -ti:3000 | xargs kill -9

# Issue: Module not found
# Fix: pip install <module>

# Issue: npm ERR! code ERESOLVE
# Fix: npm install --legacy-peer-deps

# Issue: "TypeError: Cannot read property 'token' of undefined"
# Fix: Check localStorage in browser DevTools

# Issue: CORS error
# Fix: Backend already configured, restart server

# Issue: "Connection refused"
# Fix: Ensure backend is running on port 8000
```

---

## Useful Aliases (Optional)

### For PowerShell
```powershell
# Add to $PROFILE
function start-backend { Set-Location backend; python main.py }
function start-frontend { Set-Location frontend; npm start }
function stop-ports { 
  Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
  Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
}
```

### For Bash/Zsh
```bash
# Add to ~/.bashrc or ~/.zshrc
alias start-backend="cd backend && python main.py"
alias start-frontend="cd frontend && npm start"
alias stop-ports="pkill -f 'python main.py'; pkill -f 'npm start'"
```

---

## Reference URLs

- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **API Endpoints**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Quick Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend server running
- [ ] Frontend running
- [ ] Can access http://localhost:3000
- [ ] Can access http://localhost:8000/docs
- [ ] Can register and login
- [ ] Token saved in localStorage

---

**Happy Development!** 🚀

For more info, see README_AUTHENTICATION.md
