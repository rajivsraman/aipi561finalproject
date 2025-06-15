import streamlit as st
import requests
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Titan Career Coach", layout="wide")
st.title(" Amazon Titan Career Assistant")

BASE_URL = "http://localhost:8000"

# ---------- AUTH PHASE ----------
if "token" not in st.session_state:
    st.subheader("🔐 Login or Sign Up")
    mode = st.radio("Choose Option", ["Login", "Signup"], horizontal=True)
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Username", key="user")
    with col2:
        password = st.text_input("Password", type="password", key="pass")

    if st.button("Submit"):
        endpoint = "signup" if mode == "Signup" else "login"
        res = requests.post(f"{BASE_URL}/{endpoint}", data={"username": username, "password": password})

        if res.status_code == 200:
            if mode == "Login":
                st.session_state.token = res.json()["access_token"]
                st.session_state.username = username
                st.success(" Logged in successfully.")
                #st.experimental_rerun()
            else:
                st.success(" Account created! Switch to Login.")
        else:
            st.error(res.json().get("detail", f"{mode} failed"))

else:
    st.sidebar.markdown(f" Welcome, **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    # Sidebar user guide
    st.sidebar.markdown("---")
    st.sidebar.markdown("###  User Guide")
    st.sidebar.markdown("""
    - **Resume Scoring**: Upload your resume PDF to receive AI feedback and a score out of 20.
    - **Job Matching**: Upload your resume + type your interests to get tailored job suggestions.
    - **Chat**: Ask career questions or anything else.
    - **Export Tab**: View live metrics and download session transcript as PDF.
    """)

    tabs = st.tabs(["Resume Scoring", "Job Matching", "Chat", "Metrics / Export"])
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    transcript = []

    # ---------- Resume Scoring ----------
    with tabs[0]:
        st.subheader(" Upload Resume (PDF only)")
        resume = st.file_uploader("Upload Resume", type="pdf", key="resume_score_upload")
        if st.button("Score Resume") and resume:
            res = requests.post(f"{BASE_URL}/resume/score", files={"resume": resume}, headers=headers)
            if res.status_code == 200:
                output = res.json()["response"]
                st.text_area("AI Evaluation", output, height=350)
                transcript.append(("Resume Score", output))
            else:
                st.error("Failed to score resume.")

    # ---------- Job Matching ----------
    with tabs[1]:
        st.subheader(" Job Matching")
        resume = st.file_uploader("Upload Resume (PDF)", type="pdf", key="resume_match_upload")
        interests = st.text_input("Career Interests (comma-separated)")
        if st.button("Get Job Suggestions") and resume and interests:
            res = requests.post(
                f"{BASE_URL}/jobs/recommend",
                files={"resume": resume},
                data={"interests": interests},
                headers=headers
            )
            if res.status_code == 200:
                result = res.json()["response"]
                st.text_area("Suggested Careers", result, height=350)
                transcript.append(("Job Suggestions", result))
            else:
                st.error("Error finding job suggestions.")



    # ---------- Chat ----------
    with tabs[2]:
        st.subheader(" Ask Titan")
        prompt = st.text_area("Your question or request:")
        if st.button("Send to Titan") and prompt:
            res = requests.post(f"{BASE_URL}/chat", data={"prompt": prompt}, headers=headers)
            try:
                output = res.json()["response"]
                st.text_area("Titan Says:", output, height=300)
                transcript.append((prompt, output))
            except:
                st.error("Titan is busy. Please try again.")

    # ---------- Metrics & Export ----------
    
    with tabs[3]:
        st.subheader(" Metrics + Download Report")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Live Stats & Graph")
            try:
                # Fetch metrics history
                metrics = requests.get(f"{BASE_URL}/metrics").json()

                # Unpack metrics history
                latency_values = metrics.get("latency_history", [])
                request_ids = list(range(1, len(latency_values) + 1))

                if latency_values:
                    # Line graph for latency per request
                    import matplotlib.pyplot as plt
                    import numpy as np

                    fig, ax = plt.subplots()
                    ax.plot(request_ids, latency_values, marker="o", linestyle="-", linewidth=2)
                    ax.set_xlabel("Request Number")
                    ax.set_ylabel("Latency (s)")
                    ax.set_title("⏱ Latency Per Request")
                    st.pyplot(fig)

                    # Basic stats
                    st.markdown("###  Latency Stats")
                    st.write(f"**Mean:** {np.mean(latency_values):.3f}s")
                    st.write(f"**Min:** {np.min(latency_values):.3f}s")
                    st.write(f"**Max:** {np.max(latency_values):.3f}s")
                    st.write(f"**Std Dev:** {np.std(latency_values):.3f}s")
                else:
                    st.info("No latency data yet.")

            except Exception as e:
                st.error(" Could not fetch metrics.")
                st.text(f"Error: {e}")

        with col2:
            st.markdown("### Export Full Session Transcript")
            if st.button("Download Full Session Report"):
                res = requests.post(f"{BASE_URL}/pdf/export_session", headers=headers)
                try:
                    filename = res.json()["filename"]
                    st.success(" Report Generated")
                    st.markdown(f"[ Download PDF](generated_reports/{filename})")
                except:
                    st.error(" Error generating transcript.")
