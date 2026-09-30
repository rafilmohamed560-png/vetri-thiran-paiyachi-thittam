# LegalEase AI

LegalEase is an AI-assisted legal document drafting application based on the supplied project documentation.

## Architecture

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **AI:** Google Gemini via the current `google-genai` SDK
- **Exports:** TXT, DOCX, PDF
- **Validation:** Pydantic
- **Tests:** pytest + FastAPI TestClient

The original documentation specifies Gemini 1.5 Pro. The implementation keeps the model configurable through `GEMINI_MODEL`; the default is a currently available Gemini model. This avoids hard-coding a retired/changed model identifier.

## Important legal notice

LegalEase generates drafts and legal information for assistance. It is **not a law firm and does not provide legal advice**. AI-generated text can contain errors, omissions, or jurisdiction-specific problems. A qualified lawyer should review documents before they are signed, submitted, or relied upon.

## Project structure

```text
LegalEase/
├── backend/
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── config.py
│   └── ai_core/
│       ├── __init__.py
│       └── gemini_generator.py
├── frontend/
│   └── app.py
├── utils/
│   ├── __init__.py
│   ├── document_utils.py
│   └── exporters.py
├── tests/
│   ├── test_api.py
│   └── test_exporters.py
├── assets/
│   └── logo.svg
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── requirements.txt
└── README.md
```

## 1. Prerequisites

Install Python 3.10 or newer.

Check:

```powershell
python --version
pip --version
```

## 2. Create and activate a virtual environment

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Gemini

Copy `.env.example` to `.env`:

```powershell
copy .env.example .env
```

Then set:

```env
GEMINI_API_KEY=YOUR_REAL_KEY
GEMINI_MODEL=gemini-2.5-flash
DEMO_MODE=false
BACKEND_URL=http://127.0.0.1:8000
```

For a UI/API smoke test without a Gemini key, use:

```env
DEMO_MODE=true
```

Do not commit `.env`.

## 5. Start the backend

From the project root:

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Open the FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## 6. Start the Streamlit frontend

Open a second terminal, activate the same virtual environment, then:

```bash
streamlit run frontend/app.py
```

Open:

```text
http://localhost:8501
```

## 7. Test the API manually

```bash
curl -X POST "http://127.0.0.1:8000/generate" ^
  -H "Content-Type: application/json" ^
  -d "{"document_type":"Non-Disclosure Agreement","parties":"Alice Smith (Disclosing Party), TechNova Inc. (Receiving Party)","terms":"Confidential information must be protected; No disclosure to third parties without permission; Agreement may be terminated with 15 days notice","effective_date":"2026-09-28"}"
```

On PowerShell, use `curl.exe` rather than the PowerShell alias if necessary.

## 8. Run automated tests

```bash
pytest -q
```

The tests use `DEMO_MODE=true` and therefore do not require a live Gemini API call.

## 9. Docker

Build and run:

```bash
docker compose up --build
```

The Streamlit frontend will be available at:

```text
http://localhost:8501
```

The FastAPI backend will be available at:

```text
http://localhost:8000/docs
```

Before using Docker with Gemini, put your real API key in `.env`.

## Features implemented

- Legal document generation
- Employment contract, NDA, lease and generic agreement prompts
- Parties, terms, effective date and extra instructions
- Editable document preview
- TXT export
- DOCX export with logo, headings, terms table and footer
- PDF export with logo/header/footer
- FastAPI validation and error handling
- CORS configuration
- Configurable Gemini model
- Demo mode for development/testing
- Automated API and exporter tests
- Basic privacy/security safeguards such as no API-key logging and bounded request sizes

## Production considerations

Before public deployment:

1. Add authentication and authorization.
2. Add rate limiting.
3. Use HTTPS.
4. Store secrets in a secret manager.
5. Add audit logging that excludes document contents unless legally justified.
6. Review data retention and deletion policies.
7. Add jurisdiction-specific legal templates and review them with qualified lawyers.
8. Consider asynchronous job processing for long-running generation.
9. Add abuse protection and request quotas.
10. Do not represent generated text as attorney-reviewed advice.
