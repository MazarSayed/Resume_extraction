# Resume Extraction API

A FastAPI-based service that extracts structured data from PDF resumes using Google Gemini AI.

## Features

- PDF resume upload with automatic timestamped naming
- AI-powered data extraction using Google Gemini
- Extracts: name, contact info, work experience, education, skills, and certificates
- Structured JSON output with Pydantic validation
- Interactive API documentation via Swagger UI

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Google Gemini API key

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd resume_extraction

# Install dependencies
uv sync
```

## Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL_NAME=gemini-3-flash-preview   # optional, this is the default
UPLOAD_DIR=uploads                          # optional, this is the default
```

## Running the Server

```bash
# Development server with hot reload
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and docs link |
| GET | `/health` | Health check |
| POST | `/resume/upload` | Upload a PDF resume |
| POST | `/resume/extract` | Extract data from uploaded PDF |


## Project Structure

```
resume_extraction_api/
├── main.py                 # FastAPI application entry point
├── models/
│   └── schemas.py          # Pydantic models for resume data
├── services/
│   └── gemini_service.py   # Gemini API integration
├── routes/
│   └── resume.py           # Resume upload & extract endpoints
├── utils/
│   └── helpers.py          # Utility functions
└── uploads/                # PDF storage directory (auto-created)
```


