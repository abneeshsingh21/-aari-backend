# AARI - Docker Configuration

This file enables running AARI in a Docker container for consistent deployment.

## Using Docker Compose (Recommended)

### Prerequisites
- Docker Desktop: https://www.docker.com/products/docker-desktop
- Docker Compose (usually included with Docker Desktop)

### Quick Start

```bash
# Clone repository
git clone https://github.com/abneeshsingh21/-aari-backend.git
cd -aari-backend

# Start all services
docker-compose up

# Or run in background
docker-compose up -d

# Stop services
docker-compose down
```

### Access Services

- **Backend API**: http://localhost:5000
- **Frontend**: http://localhost:8081
- **Backend Health**: http://localhost:5000/api/health

### Build Custom Image

```bash
# Build backend image
docker build -t aari-backend ./backend

# Build frontend image
docker build -t aari-frontend ./VoiceAssistantApp

# Run containers
docker run -p 5000:5000 aari-backend
docker run -p 8081:8081 aari-frontend
```

## Docker Compose Services

The `docker-compose.yml` includes:

1. **Backend Service**
   - Python Flask API
   - Port: 5000
   - Volume: `./backend:/app`

2. **Frontend Service**
   - React Native Expo
   - Port: 8081
   - Volume: `./VoiceAssistantApp:/app`

## Environment Variables

Create `.env` file before running:

```env
GOOGLE_API_KEY=your_api_key
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
BACKEND_URL=http://localhost:5000
```

## Deployment

### Deploy to Render

1. Push code to GitHub
2. Go to https://render.com
3. Create new Web Service
4. Select your repository
5. Set start command: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
6. Add environment variables
7. Deploy

### Deploy to Railway

1. Connect GitHub repository
2. Select `-aari-backend` as root directory
3. Add environment variables
4. Deploy

### Deploy to Heroku

```bash
heroku login
heroku create your-app-name
git push heroku main
heroku config:set GOOGLE_API_KEY=your_key
heroku open
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000 (Windows)
netstat -ano | findstr :5000

# Find process using port 5000 (macOS/Linux)
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Container Issues

```bash
# View container logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild containers
docker-compose build --no-cache

# Remove all containers
docker-compose down -v
```

### Permission Issues

On macOS/Linux, add executable permission:

```bash
chmod +x START_ALL.sh
chmod +x SETUP.sh
```
