# Backend - Resume Analysis API

A Flask-based REST API for analyzing and scoring resumes using Google Generative AI.

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## Environment Setup

1. **Create a `.env` file** in the `backend` directory:

```bash
GENERATIVE_API_KEY=your_google_api_key_here
```

2. **Obtain your API key:**
   - Visit [Google AI Studio](https://ai.google.dev)
   - Generate an API key for the Generative AI API
   - Add it to your `.env` file

## Launching the Backend

### Development Mode

**Using Flask development server:**

```bash
flask run --port 8000
```

Or using the WSGI entry point:

```bash
python wsgi.py
```

The server will start at `http://localhost:8000`

### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

## User Stories

**US-10: Job Description analyses by server**
- As a user,
- I want my job description to be analyzed by the server,
- so that I can receive targeted feedback on how to optimize my resume for the role.

## API Endpoints

- **GET `/`** - Health check endpoint
- **GET `/about`** - About endpoint
- **POST `/resume/upload`** - Upload and analyze resume file (PDF or DOCX). Returns a resume ID for result retrieval.
- **GET `/resume/<resume_id>/score`** - Retrieve analysis results for a resume (score, feedback, suggestions)

## Testing

Run the test suite:

```bash
pytest
```

## Project Structure

```
backend/
├── api/
│   ├── app.py           # Flask application
│   ├── models/          # Data models
│   ├── routes/          # API route definitions
│   ├── services/        # Business logic
│   └── utils/           # Utility functions
├── config/              # Configuration settings
├── tests/               # Test files
├── uploads/             # Upload directory
├── wsgi.py              # WSGI entry point
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Notes

- The API runs on `http://localhost:8000` by default
- CORS is enabled for cross-origin requests
- Uploaded files are stored in the `uploads/` directory
- Resume analysis requires a valid Google Generative AI API key
