# Quick Deployment Guide for Render

## Step-by-Step Instructions

### 1. Create a GitHub Repository

First, create a new repository on GitHub for just this backend:

1. Go to GitHub.com
2. Click "New Repository"
3. Name it: `water-quality-backend` (or any name you prefer)
4. Make it Public or Private
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create Repository"

### 2. Push Backend to GitHub

Run these commands from the `backend-render` folder:

```bash
cd backend-render

# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Water Quality Monitoring Backend"

# Add your GitHub repository as remote (replace with your actual URL)
git remote add origin https://github.com/YOUR_USERNAME/water-quality-backend.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Deploy on Render

1. **Sign up/Login to Render**
   - Go to https://render.com
   - Sign up or login (you can use your GitHub account)

2. **Create New Web Service**
   - Click "New +" in the top right
   - Select "Web Service"
   
3. **Connect GitHub Repository**
   - Click "Connect account" to connect your GitHub
   - Select the repository you just created
   - Click "Connect"

4. **Render Auto-Configuration**
   - Render will automatically detect `render.yaml`
   - It will configure everything for you:
     - Name: batmaak-backend
     - Environment: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 api:app`
   
5. **Deploy**
   - Click "Create Web Service"
   - Wait for the build and deployment (usually 2-5 minutes)
   - Once deployed, you'll see: "Your service is live 🎉"

6. **Get Your Backend URL**
   - Copy the URL shown (e.g., `https://batmaak-backend.onrender.com`)
   - This is your backend API URL

### 4. Test Your Backend

Test your deployed backend:

```bash
# Replace with your actual Render URL
curl https://your-backend-url.onrender.com/api/latest
```

You should see JSON data with water quality readings.

### 5. Connect Frontend to Backend

After deployment, you'll receive a URL like:
```
https://batmaak-backend-xyz123.onrender.com
```

Tell me this URL, and I'll update your frontend to connect to it!

## Important Notes

### Free Tier Limitations
- Render's free tier spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds to wake up
- Consider using a paid plan for production

### Monitoring
- Check logs in Render Dashboard under "Logs" tab
- Monitor performance under "Metrics" tab

### Auto-Deploy
- By default, every push to main branch auto-deploys
- Disable in Settings if you want manual deploys

## Troubleshooting

### Build Fails
- Check the build logs in Render Dashboard
- Ensure `requirements.txt` is correct
- Verify Python version compatibility

### Service Crashes
- Check the logs for error messages
- Common issue: Port binding (already handled in our code)

### CORS Errors
- Backend already has CORS enabled for all origins
- If issues persist, check browser console

## Next Steps

Once your backend is deployed:
1. Test all endpoints (`/api/latest`, `/api/historical`, `/api/alerts`)
2. Copy your Render URL
3. Update your frontend's `NEXT_PUBLIC_API_URL` to point to this URL
4. Deploy your frontend (Vercel/Netlify recommended)

## Need Help?

If you encounter any issues:
1. Check Render logs first
2. Verify all files are committed to GitHub
3. Ensure repository is connected correctly
4. Contact me with the error message from logs

