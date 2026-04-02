# 📩 Daily Email Dashboard

Automated influencer email collection system with a full web dashboard.

## Architecture

```
Google Sheets → GitHub Actions (daily 9 AM IST) → data/*.json
                                                      ↓
                                         FastAPI (Vercel) ← React (Vercel)
```

## Project Structure

```
├── backend/
│   ├── main.py          # FastAPI API
│   ├── processor.py     # Email processor (replaces all calculate_*.py)
│   ├── requirements.txt
│   └── vercel.json      # Vercel serverless config for Python
├── frontend/
│   ├── src/App.jsx      # Dashboard UI
│   ├── src/App.css      # Dark-mode styles
│   └── vercel.json      # SPA routing config
├── data/                # Daily JSON files (auto-generated)
├── .github/workflows/
│   └── daily_report.yml # Daily cron at 9 AM IST
└── migrate_historical.py # One-time: convert old Excel → JSON
```

---

## 🚀 Deployment Guide

### Step 1 — Add GitHub Secret

Go to: **GitHub Repo (`terminalyadav/Daily-Email`) → Settings → Secrets and variables → Actions → New repository secret**

| Name | Value |
|------|-------|
| `GOOGLE_CREDENTIALS_JSON` | Paste entire content of `service-account-key.json` |

### Step 2 — Deploy Backend (Vercel)

1. Go to [vercel.com](https://vercel.com) → Add New... → Project
2. Import `terminalyadav/Daily-Email`
3. Settings:
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
4. Deploy! Note your URL (e.g. `https://daily-email-backend.vercel.app`)

### Step 3 — Deploy Frontend (Vercel)

1. You can update `frontend/.env.production` with your backend URL: `VITE_API_URL=https://...` and push, OR use Vercel environment variables.
2. Go to [vercel.com](https://vercel.com) → Add New... → Project
3. Import `terminalyadav/Daily-Email`
4. Settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - Add Vercel Environment Variable: `VITE_API_URL` = `https://your-backend-url.vercel.app`
5. Deploy!

### Step 4 — Run GitHub Action

GitHub → Actions → "Daily Email Report" → **Run workflow** -> This generates today's data!

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
