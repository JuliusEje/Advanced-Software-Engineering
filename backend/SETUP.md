# Backend Setup Guide

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Supabase project with credentials
- Google Generative AI API key

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create/update `.env` file in the `backend/` directory:

```env
GENERATIVE_API_KEY=your_google_api_key_here
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
JWT_SECRET=your-secure-jwt-secret-key-change-in-production
```

### 3. Set Up Supabase Database

#### Create Users Table

```sql
CREATE TABLE IF NOT EXISTS users (
  id BIGSERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own data" ON users
  FOR SELECT USING (auth.uid()::text = id::text);
```

#### Create Resumes Table

```sql
CREATE TABLE IF NOT EXISTS resumes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  filename TEXT NOT NULL,
  file_path TEXT NOT NULL,
  score INTEGER,
  feedback TEXT,
  suggestions JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for faster queries
CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_resumes_created_at ON resumes(created_at DESC);

-- Enable RLS
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;

-- Policies: Users can only read/insert their own resumes
CREATE POLICY "Users can read own resumes" ON resumes
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can insert own resumes" ON resumes
  FOR INSERT WITH CHECK (user_id = auth.uid());
```

### 4. Run the Application

```bash
python wsgi.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication Routes

- **POST /api/auth/register** - Create new user account
  - Body: `{ "email": "", "password": "", "name": "" }`
  - Returns: `{ "token": "", "user": {...} }`

- **POST /api/auth/login** - Login user
  - Body: `{ "email": "", "password": "" }`
  - Returns: `{ "token": "", "user": {...} }`

- **POST /api/auth/logout** - Logout user (token invalidation frontend-side)
  - Requires: Valid Authorization header with Bearer token

- **GET /api/auth/verify** - Verify token validity
  - Requires: Valid Authorization header with Bearer token
  - Returns: `{ "user": {...} }`

### Resume Routes (All require authentication)

- **POST /api/resume/upload** - Upload and analyze resume
  - Headers: `Authorization: Bearer <token>`
  - Body: FormData with file
  - Returns: `{ "id": "", "score": 75, "feedback": "", "suggestions": [...] }`

- **GET /api/resume/<resume_id>/score** - Get specific resume analysis
  - Headers: `Authorization: Bearer <token>`
  - Returns: Complete analysis data

- **GET /api/resume/history** - Get all resumes for current user
  - Headers: `Authorization: Bearer <token>`
  - Returns: `{ "resumes": [...] }`

## Architecture & Design Decisions

### Security

- **JWT Authentication:** Stateless, scalable session management
- **Password Hashing:** bcrypt for secure password storage
- **Row-Level Security:** Supabase RLS ensures users only access their data
- **Token-based API:** Secure, CORS-enabled communication

### Scalability

- **Database:** Supabase provides automatic scaling and backups
- **Session Management:** Database-backed (future enhancement: add Redis)
- **File Storage:** Currently local uploads directory (future: AWS S3/GCS)
- **User Data Isolation:** Session-based route handlers

### Future Enhancements

1. **PDF Generation**
   - Save optimized resume as PDF
   - Add watermark with user information
   - Generate comparison reports

2. **Resume Storage**
   - Store resume files in cloud storage (S3/GCS)
   - Version control for resume changes
   - Archive old versions

3. **Advanced Analytics**
   - Track score improvements over time
   - Compare resume versions
   - Industry benchmarking

4. **Performance Optimization**
   - Implement Redis caching for frequently accessed data
   - Add request rate limiting
   - Optimize file processing pipeline

5. **AI/ML Enhancements**
   - Custom scoring models per industry
   - ATS (Applicant Tracking System) optimization
   - Behavioral analysis

## Deployment

### For Production

1. Set secure JWT_SECRET in environment
2. Use HTTPS for all communications
3. Enable CORS with specific frontend domain
4. Use environment-specific configurations
5. Set up monitoring and logging
6. Configure automatic database backups
7. Use environment variables for all secrets

### Docker Configuration (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=api/app.py

CMD ["python", "wsgi.py"]
```

## Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=api tests/
```

## Troubleshooting

1. **Supabase Connection Error**
   - Verify SUPABASE_URL and SUPABASE_KEY are correct
   - Check network connectivity to Supabase

2. **JWT Token Errors**
   - Ensure JWT_SECRET is set and consistent
   - Verify token format: `Bearer <token>`

3. **File Upload Issues**
   - Check uploads/ directory exists and is writable
   - Verify file size limits (currently 10MB)
   - Ensure supported file types (PDF, DOCX)

4. **AI Analysis Failures**
   - Verify GENERATIVE_API_KEY is valid
   - Check API quota limits
   - Review file encoding and format
