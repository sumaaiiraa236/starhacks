CareCrew - Final Complete Release (Embedded Keys)
================================================
<img width="735" height="520" alt="image" src="https://github.com/user-attachments/assets/c9211fdb-bea8-4240-87d5-1f9834291937" />


This package is the final CareCrew elderly-care multi-agent system prepared for demo and extension.
It includes backend services, a simple real-time frontend, demo data, and utilities. The backend/.env file
is pre-populated with keys you provided (keep this zip private).

WHAT'S INCLUDED
- backend/: FastAPI, agents (rule-based), event replay, DB helpers, bus, Pinecone seeding.
- data/: demo CSV files (health_monitoring.csv, safety_monitoring.csv, daily_reminder.csv).
- frontend/: lightweight real-time dashboard (static + WebSocket client).
- requirements.txt: Python packages to install.
- run_demo_win.ps1: PowerShell demo helper (edit if needed).

QUICK START (Guaranteed demo - SQLite, no external services required)
1. Extract this zip to a local folder (avoid OneDrive if possible):
   C:\projects\carecrew_final
2. Open Anaconda Prompt
   conda create -n carecrew python=3.10 -y
   conda activate carecrew
3. Install minimal deps:
   python -m pip install pandas python-dotenv fastapi uvicorn
   # (or install full requirements: python -m pip install -r requirements.txt)
4. Run demo:
   cd backend
   python setup_db.py
   python run_demo.py ../data/health_monitoring.csv
5. To stop: Ctrl+C

INTEGRATED MODE (Redis + Postgres + Pinecone)
- Ensure Redis is running and POSTGRES_URL (backend/.env) is correct.
- Start uvicorn api:app for WebSocket dashboard.
- Run init_db_postgres.py then seed_pinecone.py to initialize.
- Run orchestrator: python run_demo.py ../data/health_monitoring.csv

CREDITS & TOOLS
- OpenAI (or Gemini) for LLM phrasing (temperature=0)
- Pinecone for vector RAG
- FastAPI + uvicorn for realtime API / WebSocket
- Redis (optional) for message bus scaling
- SQLAlchemy + Postgres (optional) for production LTM

FLOWCHART LR
    A[Sensor Event (CSV)] -->|Publish| B(Message Bus)
    B --> C[Health Watcher Agent]
    B --> D[Safety Monitor]
    C --> E[Emergency Responder]
    D --> E
    E --> F[SQLite/Postgres LTM]
    E --> G[Reminder Manager]
    G --> F
    F --> H[Pinecone (Vector Memory)]
    H --> I[Family Liaison Agent]
    I --> J[Caregiver / Family Notifications]
    B --> K[FastAPI WS Server] --> L[React Dashboard]


