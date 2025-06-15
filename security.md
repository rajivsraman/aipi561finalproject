#  Security and Responsibility

This document outlines the security architecture, privacy controls, and responsible AI practices implemented in the **Amazon Titan Career Coach** project.

---

##  Security Measures

###  Authentication and Authorization
- **JWT-based Authentication**: All API requests require a valid JWT token. Users must log in or sign up to receive a token.
- **Role-based Access (Future)**: Role-based access control is planned for future iterations to separate admin and user privileges.

###  HTTPS and Data Encryption
- **Local Development**: While development is local, future deployments will enforce HTTPS via SSL/TLS.
- **Data-in-Transit**: All data transmitted between frontend and backend is protected by secure API gateways in deployment.

###  Input Sanitization
- All text and file inputs are validated to prevent:
  - Malicious file uploads
  - Path traversal attacks
  - XSS and injection vulnerabilities

###  Dependency Security
- Dependencies are pinned using `requirements.txt`
- Regular scans with tools like `pip-audit` are recommended before deployment

---

##  Privacy Controls

###  Data Retention
- Uploaded resumes and LinkedIn links are not stored after processing.
- Session transcripts are temporary and user-controlled (exported to PDF only upon request).

###  Personally Identifiable Information (PII)
- Resume content is processed in-memory only.
- No raw data is retained or shared externally.

---

##  Responsible AI Practices

###  Model Transparency
- The Titan model used from Amazon Bedrock is cited and versioned (`amazon.titan-text-premier-v1:0`)
- Output includes rationale for resume/job matching decisions, improving explainability.

###  Bias Mitigation
- Prompts are engineered to encourage neutral, skill-based evaluations.
- Career suggestions are framed around user interests and strengths, avoiding gendered or racial bias.

---

##  Compliance Documentation

###  GDPR-Like Principles
- Although not deployed in production, the design follows principles akin to GDPR:
  - Right to export (via PDF)
  - Right to be forgotten (session clears upon logout)
  - No persistent identifier stored without user action

###  Auditability
- Metrics are logged (total requests, latency).
- Exported reports serve as audit records with timestamps.

---

##  Incident Response Plan (Suggested for Deployment)

- Alert system for 500 errors via monitoring logs
- Rate-limiting and CAPTCHA planned for production scaling
- Logging with audit trail (UUID + timestamps) per session
