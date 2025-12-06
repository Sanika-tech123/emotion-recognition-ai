# Deployment Guide - Emotion Recognition System

## Prerequisites
- GitHub account
- Code pushed to GitHub repository

## Option 1: Render.com (Recommended - FREE)

### Step 1: Create `render.yaml` in project root

### Step 2: Push to GitHub
```bash
git add .
git commit -m "Add Render deployment config"
git push
```

### Step 3: Deploy on Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Blueprint"
4. Connect your repository
5. Render will auto-detect `render.yaml`
6. Click "Apply"
7. Wait 5-10 minutes for deployment

### Your App URLs
- Backend: `https://your-app-name.onrender.com`
- Frontend: `https://your-app-name-frontend.onrender.com`

### Important Notes
- **Free tier** has cold starts (15 sec delay after inactivity)
- Models download on first run (~5 min)
- Update `API_URL` in frontend to your backend URL

---

## Option 2: Railway.app ($5 free credit)

### Step 1: Create `Procfile`

### Step 2: Deploy
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. New Project → Deploy from GitHub
4. Select your repository
5. Add two services:
   - Backend: Set start command `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Frontend: Set start command `streamlit run frontend/streamlit_app.py --server.port $PORT`

---

## Option 3: Hugging Face Spaces (FREE with GPU!)

### Best for ML models

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Create New Space → Streamlit
3. Upload your files
4. Add `requirements.txt`
5. It auto-deploys!

**Note**: Combine frontend and backend into single Streamlit app

---

## Local Network Deployment (Quick Test)

Make your app accessible on local network:

```bash
# Backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend  
streamlit run frontend/streamlit_app.py --server.address 0.0.0.0
```

Access from any device on your network:
- `http://YOUR_IP:8501`

---

## Production Checklist

- [ ] Set environment variables for API keys
- [ ] Use production-grade server (Gunicorn for FastAPI)
- [ ] Enable HTTPS
- [ ] Add rate limiting
- [ ] Set up monitoring
- [ ] Configure CORS properly
- [ ] Add analytics

---

## Troubleshooting Deployment

**Issue**: Models taking too long to load
→ Use smaller models or cache them

**Issue**: Out of memory
→ Upgrade to paid tier or use lighter models

**Issue**: CORS errors
→ Update `allow_origins` in `main.py` to your frontend URL
