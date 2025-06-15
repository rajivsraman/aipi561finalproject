#  Deployment Guide for Titan Career Coach

This guide outlines the steps to deploy the Titan Career Coach app, which includes a FastAPI backend and a Streamlit frontend integrated with Amazon Bedrock.

---

##  Project Structure

```
.
├── backend/
├── frontend/
├── main.py
├── requirements.txt
├── README.md
├── Deployment_Guide.md
└── ...
```

---

## 1.  Prerequisites

Ensure you have the following installed:
- Python 3.10+
- pip
- AWS CLI (configured with access to Bedrock)
- Docker (optional for containerization)

---

## 2.  Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Ensure environment variables are set:

```bash
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=amazon.titan-text-premier-v1:0
export JWT_SECRET=your_secret_key
```

---

## 3.  Run the Backend (FastAPI)

```bash
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`.

---

## 4.  Run the Frontend (Streamlit)

From the root directory or `/frontend`, run:

```bash
streamlit run frontend/streamlit_app.py
```

The UI will be served at `http://localhost:8501`.

---

## 5.  Running Tests and Coverage

```bash
coverage run -m pytest
coverage report
```

To generate an HTML report:
```bash
coverage html
open htmlcov/index.html
```

---

## 6.  Optional: Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t titan-career-coach .
docker run -p 8000:8000 titan-career-coach
```

---

## 7.  Deploy to Cloud (Optional)

You may deploy to services like:
- **AWS EC2 / Lightsail**
- **Render / Railway**
- **DockerHub + ECS**

For AWS EC2:

```bash
scp -r . ec2-user@<your-ec2-ip>:/home/ec2-user/
ssh ec2-user@<your-ec2-ip>
cd /home/ec2-user
./run.sh  # or manually activate venv and run uvicorn/streamlit
```

---

## 8.  Security & IAM

- Create an IAM user with permissions for Bedrock
- Generate access keys
- Configure with `aws configure`
- Never commit secrets or `.aws/credentials` to GitHub

---

## 9.  Cleanup

To stop all processes:

```bash
pkill -f uvicorn
pkill -f streamlit
deactivate
```

To clean virtualenv:

```bash
rm -rf venv __pycache__ .pytest_cache htmlcov
```


