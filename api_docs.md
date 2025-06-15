# API Documentation

This document provides detailed information about the API endpoints for the **Titan Career Coach** backend.

---

##  Base URL

```
http://localhost:8000
```

All endpoints below are relative to this base URL.

---

##  Authentication

### `POST /signup`

- **Description**: Create a new user account.
- **Request body** (form data):
  - `username`: string
  - `password`: string
- **Responses**:
  - `200 OK`: Account created
  - `400 Bad Request`: User already exists

---

### `POST /login`

- **Description**: Log in to receive a JWT token.
- **Request body** (form data):
  - `username`: string
  - `password`: string
- **Responses**:
  - `200 OK`: Returns `access_token`
  - `401 Unauthorized`: Invalid credentials

---

##  Resume Scoring

### `POST /resume/score`

- **Description**: Submit a resume and receive a quality score and AI feedback.
- **Request**:
  - Header: `Authorization: Bearer <token>`
  - File: `resume` (PDF)
- **Responses**:
  - `200 OK`: `{ "response": "<AI feedback>" }`
  - `422 Unprocessable Entity`: Missing or invalid file

---

##  Job Matching

### `POST /jobs/recommend`

- **Description**: Recommend careers based on resume and user interests.
- **Request**:
  - Header: `Authorization: Bearer <token>`
  - File: `resume` (PDF)
  - Data: `interests` (string)
- **Responses**:
  - `200 OK`: `{ "response": "<job suggestions>" }`
  - `422 Unprocessable Entity`: Missing or malformed data

---

##  LinkedIn Analysis

### `POST /linkedin/analyze`

- **Description**: Analyze LinkedIn profile for optimization suggestions.
- **Request**:
  - Header: `Authorization: Bearer <token>`
  - Data: `link` (LinkedIn profile URL)
- **Responses**:
  - `200 OK`: `{ "response": "<optimization suggestions>" }`

---

##  Chat with Titan

### `POST /chat`

- **Description**: Send a prompt to the conversational AI.
- **Request**:
  - Header: `Authorization: Bearer <token>`
  - Data: `prompt` (text)
- **Responses**:
  - `200 OK`: `{ "response": "<chat response>" }`

---

##  Metrics

### `GET /metrics`

- **Description**: Return real-time API usage statistics.
- **Response**:
  ```json
  {
    "requests": 42,
    "last_latency_sec": 0.352,
    "timestamp": "2025-06-15T14:32:22"
  }
  ```

---

##  Export Report

### `POST /pdf/export_session`

- **Description**: Generate and export the user session transcript with metrics.
- **Request**:
  - Header: `Authorization: Bearer <token>`
- **Responses**:
  - `200 OK`: `{ "filename": "abcd1234_session.pdf" }`
  - File is saved under `generated_reports/`

---

##  Error Handling

All error responses follow this structure:

```json
{
  "detail": "Description of the error"
}
```

---

##  Authorization Notes

- All routes except `/login` and `/signup` require a valid Bearer token.
- Use `Authorization: Bearer <token>` in request headers.

