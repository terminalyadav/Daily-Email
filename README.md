# 📩 Daily Email Dashboard

Automated influencer email collection system with a full web dashboard.

## Architecture

```
Google Sheets → GitHub Actions (daily 9 AM IST) → data/*.json
                                                      ↓
                                         FastAPI (Render) ← React (Vercel)
```

## Project Structure

```
├── backend/
│   ├── main.py          # FastAPI API
│   ├── processor.py     # Email processor (replaces all calculate_*.py)
│   ├── requirements.txt
│   └── render.yaml      # Render deploy config
├── frontend/
│   ├── src/App.jsx      # Dashboard UI
│   ├── src/App.css      # Dark-mode styles
│   └── vercel.json
├── data/                # Daily JSON files (auto-generated)
├── .github/workflows/
│   └── daily_report.yml # Daily cron at 9 AM IST
└── migrate_historical.py # One-time: convert old Excel → JSON
```

---

## 🚀 Deployment Guide (One-Time Setup)

### Step 1 — Create GitHub Private Repo

```bash
git init
git add .
git commit -m "Initial commit"
# Create private repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/daily-email.git
git push -u origin main
```

### Step 2 — Add GitHub Secret

Go to: **GitHub Repo → Settings → Secrets → Actions → New secret**

| Name | Value |
|------|-------|
| `GOOGLE_CREDENTIALS_JSON` | Paste entire content of `service-account-key.json` |

### Step 3 — Deploy Backend (Render)

1. Go to [render.com](https://render.com) → New → Web Service
2. Connect your GitHub repo
3. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add env var: `GOOGLE_CREDENTIALS_JSON` = paste service account JSON
5. Deploy! Note your URL: `https://xxx.onrender.com`

### Step 4 — Deploy Frontend (Vercel)

1. Update `frontend/.env.production`: set `VITE_API_URL=https://xxx.onrender.com`
2. Commit + push
3. Go to [vercel.com](https://vercel.com) → New Project → Import GitHub repo
4. Settings:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add env var: `VITE_API_URL` = your Render backend URL
6. Deploy!

### Step 5 — Migrate Historical Data (One Time)

```bash
cd "/home/ashutosh-yadav/Desktop/Daily Email"
source venv/bin/activate
python migrate_historical.py
git add data/
git commit -m "chore: add historical data"
git push
```

### Step 6 — Test GitHub Action

GitHub → Actions → "Daily Email Report" → **Run workflow**

---

## Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# → http://localhost:8000/docs

# Frontend
cd frontend
npm install
npm run dev
# → http://localhost:5173
```
