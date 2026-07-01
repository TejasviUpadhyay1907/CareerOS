# CareerOS 🚀

An AI-powered career management platform — **fully live and working**.

---

## 🌐 Live Links

| | URL |
|--|--|
| **🖥️ Frontend** | **https://careeros-tejasvi1907.vercel.app** |
| **⚡ Backend API** | **https://careeros-api-sldq.onrender.com** |
| **📖 API Docs** | **https://careeros-api-sldq.onrender.com/docs** |
| **💻 GitHub** | **https://github.com/TejasviUpadhyay1907/CareerOS** |

> ⚠️ Backend on Render free tier — first request after 15 min inactivity takes ~30s to wake up. Refresh and try again if slow.

---

## 🔑 Demo Login

```
Email:    demo@careeros.ai
Password: Demo1234!
```

Click **"Click to fill demo credentials"** on the login page for quick access.

---

## ✅ Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Resume Intelligence** | ✅ | Upload PDF/DOCX → AI health score, domain, projects, certifications, strengths, recommendations |
| **Job Analysis** | ✅ | Paste job description → AI match %, technical fit, ATS score, skill gaps |
| **Resume Optimizer** | ✅ | AI rewrites resume bullets for a specific job, adds ATS keywords |
| **Career Advisor** | ✅ | AI chatbot with real 2026 market insights |
| **Interview Prep** | ✅ | Mock interviews, voice recording, AI feedback, progress tracking |
| **Application Tracking** | ✅ | Track applications with status, job URL, notes, kanban view |
| **Dashboard** | ✅ | Overview of all applications, resumes, and career stats |
| **Settings** | ✅ | Notification preferences, privacy settings |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS, shadcn/ui |
| **Backend** | FastAPI, Python 3.11, SQLAlchemy, SQLite |
| **AI** | OpenRouter → GPT-4o-mini (cost-effective) |
| **Auth** | JWT tokens (python-jose) |
| **File Upload** | Local filesystem (Render) |
| **Deploy Frontend** | Vercel (auto-deploy from GitHub) |
| **Deploy Backend** | Render (auto-deploy from GitHub) |

---

## 📁 Project Structure

```
CareerOS/
├── apps/
│   ├── api/                    # FastAPI backend
│   │   ├── app/
│   │   │   ├── ai/             # OpenRouter AI client
│   │   │   ├── api/v1/         # REST endpoints
│   │   │   │   ├── auth.py     # Login, register, JWT
│   │   │   │   ├── resume.py   # Upload, analyze, summary
│   │   │   │   ├── job.py      # Job analysis, matching
│   │   │   │   ├── career.py   # Career chat advisor
│   │   │   │   ├── accelerator.py  # Optimizer, cover letter
│   │   │   │   └── workflow.py # Applications, dashboard
│   │   │   ├── core/           # Config, exceptions, logging
│   │   │   ├── db/             # SQLAlchemy models
│   │   │   ├── models/         # Pydantic schemas
│   │   │   ├── repositories/   # DB access layer
│   │   │   ├── services/       # AI services (parser, optimizer, advisor...)
│   │   │   └── main.py
│   │   ├── requirements.txt
│   │   └── .env.example
│   └── web/                    # Next.js 14 frontend
│       └── src/
│           ├── app/            # Pages (App Router)
│           │   ├── login/
│           │   └── (dashboard)/
│           │       ├── resume/
│           │       ├── job-analysis/
│           │       ├── resume-optimizer/
│           │       ├── career-advisor/
│           │       ├── interview-prep/
│           │       ├── applications/
│           │       ├── dashboard/
│           │       └── settings/
│           ├── components/     # Reusable UI components
│           ├── hooks/          # React Query API hooks
│           └── lib/            # api-client, auth utilities
├── Dockerfile                  # Docker config for Render
├── package.json
└── README.md
```

---

## 🚀 Local Development

### Backend
```bash
cd apps/api
pip install -r requirements.txt
cp .env.example .env          # Add your OpenRouter API key
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd apps/web
npm install
# Create apps/web/.env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

---

## 🔧 Environment Variables

Copy `apps/api/.env.example` → `apps/api/.env` and fill in:

```env
# AI (OpenRouter — free tier available)
CAREEROS_API_KEY=sk-or-v1-...    # Get free key from https://openrouter.ai
USE_OPENROUTER=true

# Security
SECRET_KEY=your-long-random-secret-key

# Database (SQLite for local dev)
DATABASE_URL=sqlite+aiosqlite:///./careeros.db
```

---

## 📊 What the AI Actually Does

- **Resume Analysis** — Extracts skills, experience, projects, certifications from your PDF/DOCX. Calculates a health score across 10 dimensions. Identifies strengths and improvement areas.
- **Job Matching** — Compares your resume skills vs job requirements. Gives match %, ATS score, missing keywords, skill gap analysis.
- **Resume Optimizer** — Rewrites your experience bullets with stronger verbs and adds ATS keywords specific to the target job.
- **Career Advisor** — Personalized chat based on your uploaded resume and applications. Gives 2026-relevant advice.
- **Interview Prep** — Generates questions based on your background. Records your spoken answers via browser mic and gives AI feedback.
