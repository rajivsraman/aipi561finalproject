from fastapi import FastAPI, UploadFile, Form, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime
import os, json, time, jwt
from fastapi import File

from backend.resume_scoring import score_resume_pdf
from backend.job_recommend import recommend_jobs_from_resume
from backend.linkedin_analyzer import analyze_linkedin
from backend.report_generator import SessionTranscript
from backend.monitor import monitor_middleware
from backend.titan_client import query_titan

app = FastAPI()
app.middleware("http")(monitor_middleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

USERS_FILE, SECRET_KEY, ALGORITHM = "users.json", os.getenv("JWT_SECRET", "secret"), "HS256"
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

def load_users():
    return json.load(open(USERS_FILE)) if os.path.exists(USERS_FILE) else {}

def save_users(u): json.dump(u, open(USERS_FILE, "w"))

def create_token(u): return jwt.encode({"sub":u,"exp":time.time()+3600}, SECRET_KEY, ALGORITHM)

def verify_token(t=Depends(oauth2)):
    try: return jwt.decode(t, SECRET_KEY, [ALGORITHM])["sub"]
    except: raise HTTPException(401,"Invalid token")

session = SessionTranscript()

@app.post("/signup")
def signup(username: str=Form(...), password: str=Form(...)):
    u = load_users()
    if username in u: raise HTTPException(400,"Exists")
    u[username] = password; save_users(u)
    return {"msg":"Created"}

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    u=load_users()
    if u.get(form.username)==form.password:
        return {"access_token": create_token(form.username), "token_type":"bearer"}
    raise HTTPException(401,"Invalid credentials")

@app.post("/resume/score")
#async def score(r:UploadFile, user=Depends(verify_token))
async def score(resume: UploadFile = File(...), user: str = Depends(verify_token)):
    ans = await score_resume_pdf(resume)
    session.add("Resume Score", ans); return {"response": ans}

@app.post("/jobs/recommend")
#async def recommend(r: UploadFile, interests: str = Form(...), user=Depends(verify_token)):
async def recommend(resume: UploadFile = File(...), interests: str = Form(...), user: str = Depends(verify_token)):
    ans = await recommend_jobs_from_resume(resume, interests)
    session.add("Job Suggestions", ans); return {"response": ans}

@app.post("/linkedin/analyze")
async def linkedin(r: UploadFile, user=Depends(verify_token)):
    ans = await analyze_linkedin(r)
    session.add("LinkedIn Matches", ans); return {"response": ans}

@app.post("/chat")
async def chat(prompt: str=Form(...), user=Depends(verify_token)):
    ans = query_titan(prompt)
    session.add(prompt, ans)
    return {"response": ans}

@app.post("/pdf/export_session")
async def export_session(request: Request, user: str = Depends(verify_token)):
    metrics = {
        "requests": getattr(request.app.state, "request_count", 0),
        "last_latency_sec": round(getattr(request.app.state, "last_latency", 0.0), 2),
        "latency_history": [round(x, 3) for x in getattr(request.app.state, "latency_history", [])]
    }
    filename = session.generate_pdf(session_title=f"Career Coach Report - {user}", metrics=metrics)
    return {"filename": filename}


@app.get("/metrics")
def get_metrics(request: Request):
    history = getattr(request.app.state, "latency_history", [])
    return {
        "requests": request.app.state.request_count,
        "last_latency_sec": round(request.app.state.last_latency, 2),
        "latency_history": [round(l, 3) for l in history],
        "timestamp": datetime.now().isoformat()
    }

