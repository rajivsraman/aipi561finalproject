#  User Guide: Titan Career Assistant

Welcome to the **Titan Career Assistant**, a comprehensive career coaching platform powered by Amazon Titan via AWS Bedrock. This guide will walk you through the available features, how to use them effectively, and how to navigate the interface.

---

##  Authentication

### Login / Signup
- On launch, you are prompted to either log in or create an account.
- Provide a **username** and **password**, then click **Submit**.
- After login, you will see a personalized welcome message and gain access to all tabs in the assistant.

---

##  Tabs Overview

### 1.  Resume Scoring
- Upload a PDF resume.
- Click **Score Resume**.
- The assistant will return an evaluation and a **score out of 10**, along with actionable feedback.

### 2.  Job Matching
- Upload your resume again.
- Enter **career interests** (e.g., "Data Science, Finance").
- Click **Get Job Suggestions**.
- The assistant recommends roles that match your profile and interests with rationale and scoring.

### 3.  LinkedIn Analysis
- Paste your LinkedIn profile URL.
- Click **Analyze LinkedIn**.
- Receive feedback on how your LinkedIn profile compares with successful professionals in your desired field.

### 4.  Chat with Titan
- Ask any career-related questions.
- Use natural language (e.g., “How do I negotiate a job offer?”).
- The assistant responds with personalized, real-time advice.

### 5.  Metrics + Export
- View live system metrics including request count and latency.
- Click **Download Full Session Report** to get a PDF transcript of your session with server statistics embedded.

---

##  Transcript Export

- The full session, including questions and responses, is stored temporarily.
- When clicking **Download Full Session Report**, a professional-grade PDF is generated.

---

##  Notes

- **PDF Format**: Resume must be uploaded in `.pdf` format.
- **Latency**: All requests display the last known latency and total session usage stats.
- **Security**: Your login credentials and session data are handled securely (see `security.md`).

---

##  Tips

- Be specific with career interests (e.g., "AI Product Management" > "Technology").
- Use the chat tab to refine job suggestions based on feedback.
- Combine resume scoring + LinkedIn analysis for the best job-matching results.
- If you encounter issues, ensure your resume is a valid PDF and the server is running locally.
- For account support or troubleshooting, refer to the `README.md` and `security.md`.


