# AIPI 561 (Operationalizing AI) - Final Project
### Author: Rajiv Raman
### Institution: Duke University
### Date: June 15th, 2025

## Overview

An AI-powered career assistant platform that leverages Amazon Bedrock’s Titan model to help users:
- Score resumes with AI feedback
- Get job recommendations tailored to interests
- Analyze LinkedIn profiles
- Ask a career-focused chatbot
- Export reports and monitor usage

---

##  Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **AI Model:** Amazon Bedrock – Titan Text Premier
- **PDF Generation:** `fpdf`
- **Authentication:** JWT
- **Metrics Monitoring:** Custom Middleware
- **Deployment:** (Optional: Docker/AWS deployment options)

---

##  Architecture

```
Frontend (Streamlit) ---> FastAPI Backend ---> Amazon Bedrock Titan API
                         |         |
                         |         --> PDF Generator, Metrics Tracker
                         |
                  Resume/Job/Chat/File Routes
```

---

## Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/titan-career-coach.git
cd titan-career-coach
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Run Backend**
```bash
cd backend
uvicorn main:app --reload
```

4. **Run Frontend**
```bash
cd ../frontend
streamlit run main.py
```

---

##  Usage

- Visit Streamlit UI
- Sign up / Log in
- Use tabs to score resumes, match jobs, analyze LinkedIn, chat with Titan, and export reports
- Monitor request count and latency

---

##  Testing

- Manual test cases for each endpoint (to be expanded with Pytest)
- Validate:
  - Auth flow (signup/login)
  - Resume scoring
  - Job match + PDF upload
  - PDF report generation
  - Metrics graph rendering

---

##  Performance

- < 1s latency on average (measured via custom middleware)
- Responsive UI on resume uploads and chat

---

##  Security & Privacy

- JWT-secured endpoints
- No user data stored beyond session
- IAM restrictions in Bedrock access
- Input/output logging disabled in production
- Compliant with Responsible AI guidelines


