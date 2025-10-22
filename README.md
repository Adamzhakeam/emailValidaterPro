# Water Quality Monitoring Backend - Render Deployment

This is a standalone Flask backend API for the Water Quality Monitoring Dashboard, ready for deployment on Render.

## Features

- Real-time water quality sensor data generation
- Historical data tracking
- Alert system for critical water quality parameters
- CORS-enabled for cross-origin requests
- Automatic data updates every 60 seconds

## API Endpoints

- `GET /api/latest` - Get the most recent sensor reading
- `GET /api/historical` - Get historical sensor readings (last 100 by default)
- `GET /api/alerts` - Get recent alerts (last 10 by default)

## Deployment to Render

### Option 1: Deploy from GitHub (Recommended)

1. **Push this folder to a GitHub repository**
   ```bash
   cd backend-render
   git init
   git add .
   git commit -m "Initial commit: Water quality backend"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select this repository

3. **Configure the service**
   Render will automatically detect the `render.yaml` file and configure:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 api:app`
   - Plan: Free

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your backend
   - You'll receive a public URL like: `https://batmaak-backend.onrender.com`

### Option 2: Manual Deployment

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Choose "Build and deploy from a Git repository"
4. Configure manually:
   - **Name**: batmaak-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 api:app`
   - **Plan**: Free

## Local Development

To test the backend locally before deployment:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python api.py
```

The API will be available at `http://localhost:5000`

## Environment Variables

Currently, no environment variables are required. The application runs with default settings.

## Files Included

- `api.py` - Main Flask application with API routes
- `water_sensor_simulator.py` - Generates realistic water quality data
- `data_store.py` - Handles data persistence and alerts
- `kisa_utils.py` - Utility functions for timestamps
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment configuration
- `.gitignore` - Git ignore patterns

## After Deployment

Once deployed, your backend URL will be something like:
```
https://batmaak-backend.onrender.com
```

Use this URL to connect your frontend by updating the `NEXT_PUBLIC_API_URL` environment variable in your Next.js application.

## Water Quality Parameters Monitored

- Temperature (°C)
- Turbidity (NTU)
- pH Level
- Residual Chlorine (mg/L)
- E. coli (CFU/100mL)
- Total Coliforms (CFU/100mL)
- Ammonia (mg/L)
- Iron (mg/L)
- Manganese (mg/L)
- And 12 more parameters...

## Alert Thresholds

### Critical Alerts
- E. coli > 100 CFU/100mL
- Turbidity > 30 NTU
- pH < 5 or pH > 9
- Total Coliforms > 50 CFU/100mL

### Warning Alerts
- Turbidity: 10-30 NTU
- Residual Chlorine < 0.2 mg/L
- pH: < 6.5 or > 8.5
- Iron > 0.3 mg/L
- Manganese > 0.1 mg/L
- Ammonia > 0.5 mg/L

## Support

For issues or questions, please refer to the main project documentation.

