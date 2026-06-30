# CareerOS 🚀

An AI-powered career management platform — live at:

🌐 **Frontend:** https://careeros-tejasvi1907.vercel.app  
⚡ **Backend API:** https://careeros-api-eo94.onrender.com  
📖 **API Docs:** https://careeros-api-eo94.onrender.com/docs  
💻 **GitHub:** https://github.com/TejasviUpadhyay1907/CareerOS

---

## Features

- **Resume Intelligence** — Upload resume, AI health scoring, skills extraction
- **Job Analysis** — Paste any job description, get AI match % and ATS score
- **Resume Optimizer** — AI rewrites your resume bullets for a specific job
- **Career Advisor** — AI chatbot with 2026 market insights
- **Interview Prep** — AI mock interviews, voice recording, progress tracking
- **Application Tracking** — Kanban board, timeline, task management

## Tech Stack

| Layer    | Tech |
|----------|------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS |
| Backend  | FastAPI, Python, SQLAlchemy |
| Database | Supabase (PostgreSQL) |
| Storage  | Supabase Storage |
| AI       | OpenRouter (GPT-4o-mini) |
| Auth     | JWT tokens |
| Deploy   | Vercel (frontend) + Render (backend) |

## Project Structure

```
CareerOS/
├── apps/
│   ├── api/              # FastAPI backend
│   │   ├── app/
│   │   │   ├── ai/       # OpenRouter AI client
│   │   │   ├── api/v1/   # REST endpoints
│   │   │   ├── core/     # Config, auth, logging
│   │   │   ├── db/       # SQLAlchemy models
│   │   │   ├── models/   # Pydantic schemas
│   │   │   ├── repositories/
│   │   │   ├── services/ # AI services
│   │   │   └── main.py
│   │   └── requirements.txt
│   └── web/              # Next.js frontend
│       └── src/
│           ├── app/      # Pages
│           ├── components/
│           ├── hooks/    # API hooks
│           └── lib/
└── README.md
```

## Local Development

### Backend
```bash
cd apps/api
pip install -r requirements.txt
cp .env.example .env          # fill in your keys
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

### Demo Login
```
Email:    demo@careeros.ai
Password: Demo1234!
```

## Environment Variables

See `apps/api/.env.example` for all required variables.

Get a free AI key at https://openrouter.ai
