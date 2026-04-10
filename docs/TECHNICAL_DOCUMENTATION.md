# Technical Documentation
# AI-Based Resume Analysis and Optimization Web Application

**Version:** 2.0  
**Last Updated:** April 2026  
**Project Type:** Full-Stack Web Application  
**Development Team:** Hugo Cui (Full-Stack Developer & Project Manager), Julius (Full-Stack Developer - Data-focused)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Frontend Architecture](#frontend-architecture)
5. [Backend Architecture](#backend-architecture)
6. [Database Design](#database-design)
7. [API Documentation](#api-documentation)
8. [Authentication & Security](#authentication--security)
9. [AI Integration](#ai-integration)
10. [UI/UX Components](#uiux-components)
11. [Deployment Architecture](#deployment-architecture)
12. [Development Workflow](#development-workflow)
13. [Testing Strategy](#testing-strategy)
14. [Performance Optimization](#performance-optimization)
15. [Future Enhancements](#future-enhancements)

---

## Executive Summary

The AI-Based Resume Analysis and Optimization Web Application is a professional-grade platform designed to help job seekers improve their resumes through AI-powered analysis. The system provides:

- **Intelligent Resume Scoring**: 0-100 scoring system with detailed feedback
- **Actionable Suggestions**: 3-5 specific improvement recommendations
- **Secure User Management**: JWT-based authentication with session persistence
- **Resume History**: Track all previous analyses and improvements
- **Modern UI/UX**: Responsive design with engaging animations and interactions

### Key Metrics
- **Response Time**: < 5 seconds for resume analysis
- **Supported Formats**: PDF, DOCX
- **Security**: JWT tokens, bcrypt password hashing, Row-Level Security
- **Scalability**: Cloud-ready architecture with Supabase backend

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Vue 3 SPA (TypeScript)                              │  │
│  │  - Vue Router (Client-side routing)                  │  │
│  │  - Pinia (State management)                          │  │
│  │  - Axios (HTTP client)                               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS/REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Flask REST API (Python)                             │  │
│  │  - Authentication middleware                         │  │
│  │  - File upload handling                              │  │
│  │  - Business logic                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
┌──────────────────────┐    ┌──────────────────────┐
│   Data Layer         │    │   AI Service Layer   │
│  ┌────────────────┐  │    │  ┌────────────────┐  │
│  │ Supabase       │  │    │  │ Google         │  │
│  │ (PostgreSQL)   │  │    │  │ Generative AI  │  │
│  │ - Users        │  │    │  │ (Gemini)       │  │
│  │ - Resumes      │  │    │  └────────────────┘  │
│  │ - RLS Policies │  │    │                      │
│  └────────────────┘  │    └──────────────────────┘
└──────────────────────┘
```

### Architecture Principles

1. **Separation of Concerns**: Clear boundaries between frontend, backend, and data layers
2. **Stateless API**: RESTful design with JWT for session management
3. **Security First**: Authentication, authorization, and data encryption at every layer
4. **Scalability**: Cloud-native design ready for horizontal scaling
5. **Maintainability**: Modular code structure with clear responsibilities

---

## Technology Stack

### Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Vue.js | 3.4+ | Progressive JavaScript framework |
| TypeScript | 5.3+ | Static typing and enhanced IDE support |
| Vite | 5.0+ | Build tool and development server |
| Vue Router | 4.2+ | Client-side routing with guards |
| Pinia | 2.1+ | State management (Vuex successor) |
| Axios | 1.6+ | HTTP client for API communication |

### Backend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Backend programming language |
| Flask | 3.0+ | Lightweight web framework |
| Flask-CORS | 4.0+ | Cross-Origin Resource Sharing |
| PyJWT | 2.8+ | JSON Web Token implementation |
| Bcrypt | 4.1+ | Password hashing |
| python-docx | 1.1+ | DOCX file parsing |
| PyPDF2 | 3.0+ | PDF file parsing |

### Database & Cloud Services

| Service | Purpose |
|---------|---------|
| Supabase | PostgreSQL database with built-in auth |
| Google Generative AI | AI-powered resume analysis (Gemini) |

### Development Tools

| Tool | Purpose |
|------|---------|
| Git | Version control |
| npm | Frontend package management |
| pip | Backend package management |
| ESLint | JavaScript/TypeScript linting |
| Prettier | Code formatting |

---

## Frontend Architecture

### Directory Structure

```
frontend/
├── src/
│   ├── api/                    # API client layer
│   │   ├── client.ts          # Axios instance with interceptors
│   │   └── resume.ts          # Resume-specific API calls
│   ├── components/            # Reusable Vue components
│   │   ├── DanmakuTestimonials.vue
│   │   ├── JobInsightCard.vue
│   │   └── TypingEffect.vue
│   ├── router/                # Vue Router configuration
│   │   └── index.ts           # Routes and navigation guards
│   ├── stores/                # Pinia state management
│   │   ├── auth.ts            # Authentication state
│   │   └── resume.ts          # Resume data state
│   ├── types/                 # TypeScript type definitions
│   │   └── index.ts           # Shared interfaces
│   ├── views/                 # Page components
│   │   ├── Home.vue           # Landing page
│   │   ├── Login.vue          # User login
│   │   ├── Register.vue       # User registration
│   │   ├── Upload.vue         # Resume upload
│   │   ├── Result.vue         # Analysis results
│   │   └── History.vue        # Resume history
│   ├── App.vue                # Root component
│   ├── main.ts                # Application entry point
│   └── style.css              # Global styles
├── index.html                 # HTML entry point
├── vite.config.ts             # Vite configuration
├── tsconfig.json              # TypeScript configuration
└── package.json               # Dependencies and scripts
```

### State Management Architecture

#### Auth Store (`stores/auth.ts`)

**State:**
- `user`: Current user object (User | null)
- `token`: JWT authentication token
- `isLoading`: Loading state for async operations
- `error`: Error messages

**Computed Properties:**
- `isAuthenticated`: Boolean indicating full authentication
- `isLoggedIn`: Boolean indicating token presence

**Actions:**
- `register(email, password, name)`: User registration
- `login(email, password)`: User authentication
- `logout()`: Clear session and token
- `verifyToken()`: Validate existing token
- `setToken(token)`: Store JWT token

#### Resume Store (`stores/resume.ts`)

**State:**
- `currentScore`: Current resume analysis result
- `isLoading`: Loading state for analysis

**Actions:**
- `setScore(score)`: Update current score
- `setLoading(loading)`: Update loading state

### Routing Architecture

```typescript
Routes:
├── / (Home)                    # Public - Landing page
├── /login                      # Public - User login
├── /register                   # Public - User registration
├── /upload                     # Protected - Resume upload
├── /result/:id                 # Protected - Analysis results
└── /history                    # Protected - Resume history
```

**Navigation Guards:**
- Authentication check before protected routes
- Redirect to login if unauthenticated
- Token verification on app initialization

### API Client Architecture

**Base Configuration:**
```typescript
baseURL: 'http://127.0.0.1:8000'
timeout: 30000ms
```

**Request Interceptor:**
- Automatically attach JWT token from localStorage
- Set Authorization header: `Bearer <token>`

**Error Handling:**
- Centralized error responses
- Token expiration detection
- Automatic logout on 401 errors

---

## Backend Architecture

### Directory Structure

```
backend/
├── api/
│   ├── __init__.py
│   ├── app.py                 # Main Flask application
│   ├── models.py              # Database models
│   ├── auth/                  # Authentication module
│   │   ├── __init__.py
│   │   └── routes.py          # Auth endpoints
│   ├── routes/                # API route handlers
│   ├── services/              # Business logic
│   └── utils/                 # Helper functions
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration management
├── tests/
│   ├── conftest.py            # Test configuration
│   └── test_app.py            # Unit tests
├── uploads/                   # Local file storage
├── requirements.txt           # Python dependencies
├── wsgi.py                    # WSGI entry point
└── .env                       # Environment variables
```

### Core Components

#### 1. Flask Application (`app.py`)

**Key Features:**
- CORS enabled for cross-origin requests
- File upload handling with secure filenames
- JWT token validation middleware
- Error handling and logging

**Middleware:**
- `@token_required`: Decorator for protected endpoints
- Request validation
- Response formatting

#### 2. Authentication System

**Password Security:**
- Bcrypt hashing with salt rounds
- No plaintext password storage
- Secure password comparison

**JWT Token Structure:**
```json
{
  "user_id": 123,
  "email": "user@example.com",
  "exp": 1234567890
}
```

**Token Lifecycle:**
1. Generated on login/register
2. Stored in localStorage (client)
3. Sent in Authorization header
4. Validated on each protected request
5. Expired after configured duration

#### 3. File Processing Pipeline

**Upload Flow:**
```
1. Receive file → 2. Validate format → 3. Generate UUID
     ↓
4. Secure filename → 5. Save to disk → 6. Extract text
     ↓
7. Send to AI → 8. Parse response → 9. Store in DB
     ↓
10. Return analysis → 11. Clean up (optional)
```

**Supported Formats:**
- **PDF**: Extracted using PyPDF2
- **DOCX**: Extracted using python-docx

#### 4. AI Integration Service

**Google Generative AI (Gemini):**
- Model: `gemini-2.0-flash-exp`
- Temperature: 0.7 (balanced creativity)
- Max tokens: Configurable

**Prompt Engineering:**
```
Analyze this resume and provide:
1. Overall score (0-100)
2. Detailed feedback
3. 3-5 specific improvement suggestions

Resume content: {text}
```

**Response Parsing:**
- JSON extraction from AI response
- Fallback parsing for non-JSON responses
- Error handling for malformed responses

---

## Database Design

### Schema Overview

#### Users Table

```sql
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**Indexes:**
- Primary key on `id`
- Unique index on `email`

**Constraints:**
- Email must be unique
- Password hash required
- Timestamps auto-managed

#### Resumes Table

```sql
CREATE TABLE resumes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  filename TEXT NOT NULL,
  file_path TEXT NOT NULL,
  score INTEGER CHECK (score >= 0 AND score <= 100),
  feedback TEXT,
  suggestions JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**Indexes:**
- Primary key on `id`
- Foreign key index on `user_id`
- Index on `created_at` for sorting

**Constraints:**
- Score range: 0-100
- Cascade delete when user deleted
- JSONB for flexible suggestions storage

### Row-Level Security (RLS)

**Policy: Users can only access their own resumes**

```sql
CREATE POLICY "Users can view own resumes"
ON resumes FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own resumes"
ON resumes FOR INSERT
WITH CHECK (auth.uid() = user_id);
```

### Data Relationships

```
users (1) ──────< (N) resumes
  │
  └─ One user can have multiple resumes
  └─ Each resume belongs to one user
  └─ Cascade delete: removing user removes all resumes
```

---


## API Documentation

### Base URL
```
Development: http://localhost:8000
Production: https://api.resumeoptimizer.com
```

### Authentication Endpoints

#### POST /auth/register
Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response (201):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Errors:**
- `400`: Email already exists
- `400`: Invalid email format
- `400`: Password too weak

---

#### POST /auth/login
Authenticate existing user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Errors:**
- `401`: Invalid credentials
- `404`: User not found

---

#### POST /auth/logout
Invalidate current session.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

---

#### GET /auth/verify
Verify JWT token validity.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Errors:**
- `401`: Token expired
- `401`: Invalid token

---

### Resume Management Endpoints

#### POST /resume/upload
Upload and analyze a resume.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request (Form Data):**
```
file: <resume.pdf or resume.docx>
company: "Google" (optional)
job_description: "Software Engineer position..." (optional)
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Resume uploaded and analyzed successfully",
  "score": 85,
  "feedback": "Your resume demonstrates strong technical skills...",
  "suggestions": [
    "Add quantifiable achievements to your work experience",
    "Include relevant certifications",
    "Optimize keywords for ATS systems"
  ]
}
```

**Errors:**
- `400`: No file provided
- `400`: Invalid file format
- `401`: Unauthorized
- `500`: Analysis failed

---

#### GET /resume/:id/score
Retrieve analysis results for a specific resume.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "resume.pdf",
  "score": 85,
  "feedback": "Your resume demonstrates strong technical skills...",
  "suggestions": [
    "Add quantifiable achievements",
    "Include certifications",
    "Optimize ATS keywords"
  ],
  "created_at": "2026-04-06T10:30:00Z"
}
```

**Errors:**
- `401`: Unauthorized
- `403`: Access denied (not owner)
- `404`: Resume not found

---

#### GET /resume/history
Retrieve all resumes for authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit`: Number of results (default: 50)
- `offset`: Pagination offset (default: 0)
- `sort`: Sort order (default: created_at DESC)

**Response (200):**
```json
{
  "resumes": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "resume_v2.pdf",
      "score": 85,
      "feedback": "Strong technical background...",
      "suggestions": ["Add metrics", "Include certs"],
      "created_at": "2026-04-06T10:30:00Z",
      "updated_at": "2026-04-06T10:30:00Z"
    }
  ],
  "total": 5,
  "limit": 50,
  "offset": 0
}
```

**Errors:**
- `401`: Unauthorized

---

#### GET /resume/:id/download
Get signed URL to download resume file.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "url": "https://storage.example.com/resumes/550e8400...",
  "expires_at": "2026-04-06T11:30:00Z"
}
```

**Errors:**
- `401`: Unauthorized
- `403`: Access denied
- `404`: File not found

---

### Health Check Endpoints

#### GET /health
Check API health status.

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2026-04-06T10:30:00Z",
  "version": "2.0"
}
```

---

## Authentication & Security

### Security Measures

#### 1. Password Security
- **Hashing Algorithm**: Bcrypt with 12 salt rounds
- **Storage**: Only hashed passwords stored in database
- **Validation**: Minimum 8 characters, complexity requirements
- **Comparison**: Constant-time comparison to prevent timing attacks

#### 2. JWT Token Security
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Secret Key**: Environment variable, rotated regularly
- **Expiration**: 24 hours (configurable)
- **Claims**: user_id, email, issued_at, expires_at
- **Storage**: localStorage (client-side)

#### 3. API Security
- **CORS**: Configured for specific origins
- **Input Validation**: All inputs sanitized
- **SQL Injection**: Parameterized queries via Supabase
- **XSS Protection**: Content Security Policy headers

#### 4. Database Security
- **Row-Level Security (RLS)**: Users can only access own data
- **Encrypted Connections**: SSL/TLS for all database connections
- **Backup Strategy**: Automated daily backups via Supabase
- **Access Control**: Principle of least privilege

#### 5. File Upload Security
- **File Type Validation**: Whitelist approach (PDF, DOCX only)
- **Filename Sanitization**: Secure_filename() to prevent path traversal
- **Size Limits**: Maximum 10MB per file
- **Virus Scanning**: Planned for production
- **Storage Isolation**: UUID-based filenames prevent collisions

### Authentication Flow

```
┌─────────┐                                    ┌─────────┐
│ Client  │                                    │ Server  │
└────┬────┘                                    └────┬────┘
     │                                              │
     │  1. POST /auth/login                        │
     │  { email, password }                        │
     ├────────────────────────────────────────────>│
     │                                              │
     │                          2. Verify password │
     │                          3. Generate JWT    │
     │                                              │
     │  4. Return { token, user }                  │
     │<────────────────────────────────────────────┤
     │                                              │
     │  5. Store token in localStorage             │
     │                                              │
     │  6. GET /resume/history                     │
     │  Authorization: Bearer <token>              │
     ├────────────────────────────────────────────>│
     │                                              │
     │                          7. Validate token  │
     │                          8. Check user_id   │
     │                          9. Query database  │
     │                                              │
     │  10. Return user's resumes                  │
     │<────────────────────────────────────────────┤
     │                                              │
```

### Token Refresh Strategy

**Current Implementation:**
- Tokens expire after 24 hours
- User must re-login after expiration

**Planned Enhancement:**
- Refresh token mechanism
- Sliding session window
- Remember me functionality

---

## AI Integration

### Google Generative AI (Gemini)

#### Configuration

```python
Model: gemini-2.0-flash-exp
Temperature: 0.7
Max Output Tokens: 2048
Safety Settings: Default
```

#### Prompt Engineering

**System Prompt:**
```
You are an expert resume reviewer and career coach. Analyze the provided resume and provide constructive feedback.

Your response must be in JSON format with the following structure:
{
  "score": <integer 0-100>,
  "feedback": "<detailed overall feedback>",
  "suggestions": ["<suggestion 1>", "<suggestion 2>", ...]
}

Scoring Criteria:
- Content Quality (30%): Relevance, clarity, achievements
- Structure (20%): Organization, formatting, readability
- Keywords (20%): Industry-relevant terms, ATS optimization
- Experience (15%): Depth and relevance of work history
- Skills (15%): Technical and soft skills presentation
```

**User Prompt Template:**
```
Resume Content:
{resume_text}

Job Description (if provided):
Company: {company}
Description: {job_description}

Provide detailed analysis and actionable suggestions.
```

#### Response Processing

**Parsing Strategy:**
1. Attempt JSON extraction from response
2. Use regex to find JSON blocks
3. Fallback to structured text parsing
4. Validate score range (0-100)
5. Ensure 3-5 suggestions provided

**Error Handling:**
- API timeout: Retry with exponential backoff
- Invalid response: Return default feedback
- Rate limiting: Queue requests
- Model unavailable: Fallback to rule-based analysis

#### Performance Optimization

**Caching Strategy:**
- Cache identical resume analyses for 24 hours
- Use resume content hash as cache key
- Reduce API calls and costs

**Batch Processing:**
- Queue multiple resume analyses
- Process in parallel when possible
- Rate limit compliance

---

## UI/UX Components

### Custom Vue Components

#### 1. TypingEffect.vue
**Purpose**: Animated typing effect for hero section

**Features:**
- Simulates AI typing with variable speed (30-80ms per character)
- Blinking cursor animation
- Message rotation every 3-5 seconds
- Smooth fade-out transitions

**Messages:**
```javascript
[
  "Ready to land your dream job?",
  "When do we start optimizing?",
  "Your resume deserves better...",
  "Let's make recruiters notice you!",
  "Time to stand out from the crowd?",
  "Ready to level up your career?"
]
```

**Technical Implementation:**
- Vue 3 Composition API
- Reactive state management
- CSS animations for cursor
- Cleanup on component unmount

---

#### 2. DanmakuTestimonials.vue
**Purpose**: Floating testimonial messages (bullet-screen style)

**Features:**
- Continuous horizontal scrolling animation
- Random vertical positioning
- Variable animation speeds (12-18 seconds)
- Pause on hover
- Negative animation delay for instant appearance
- 80/20 split: Student testimonials vs Professor feedback

**Configuration:**
```javascript
maxMessages: 10
spawnDelay: 2500ms
containerHeight: 450px
messageHeight: 50px
```

**Animation Strategy:**
- CSS keyframe animations
- Negative `animation-delay` for pre-positioned messages
- Dynamic style binding for position and duration
- Smooth hover interactions

---

#### 3. JobInsightCard.vue
**Purpose**: Personalized job search motivation card

**Features:**
- Random tech job title selection
- Typing animation effect
- Gradient background matching brand colors
- Click-to-navigate to upload page
- Fade-in entrance animation

**Job Titles Pool:**
```javascript
[
  "Software Engineer",
  "Data Scientist",
  "Frontend Developer",
  "DevOps Engineer",
  "Product Manager",
  "Full Stack Developer",
  "Machine Learning Engineer",
  "Backend Developer"
]
```

**Message Templates:**
```javascript
[
  "You're so close to landing that {job} role!",
  "Almost there! That {job} position is within reach!",
  "Your next {job} opportunity is just around the corner!",
  "Keep going! You're ready for that {job} role!",
  "That {job} position? You've got this!",
  "Ready to ace that {job} interview?"
]
```

---

### Design System

#### Color Palette

**Primary Colors:**
```css
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--primary-purple: #667eea;
--primary-dark: #764ba2;
```

**Neutral Colors:**
```css
--background: #f8f9fa;
--text-primary: #1a202c;
--text-secondary: #718096;
--text-muted: #a0aec0;
--border: #e2e8f0;
```

**Semantic Colors:**
```css
--success: #48bb78;
--warning: #ecc94b;
--error: #fc8181;
--info: #3182ce;
```

#### Typography

**Font Stack:**
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 
             Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
```

**Type Scale:**
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
```

#### Spacing System

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

#### Animation Timing

```css
--transition-fast: 0.15s;
--transition-base: 0.2s;
--transition-slow: 0.3s;
--transition-slower: 0.4s;
```

---


## Deployment Architecture

### Development Environment

**Frontend:**
```bash
npm run dev
# Runs on http://localhost:3000
# Hot module replacement enabled
# Source maps for debugging
```

**Backend:**
```bash
python wsgi.py
# Runs on http://localhost:8000
# Debug mode enabled
# Auto-reload on file changes
```

**Environment Variables (.env):**
```env
# Backend
GENERATIVE_API_KEY=your_google_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
JWT_SECRET=your-secret-key-change-in-production
FLASK_ENV=development

# Frontend (optional)
VITE_API_URL=http://localhost:8000
```

---

### Production Deployment

#### Frontend Deployment (Vercel/Netlify)

**Build Configuration:**
```json
{
  "build": {
    "command": "npm run build",
    "output": "dist"
  },
  "env": {
    "VITE_API_URL": "https://api.resumeoptimizer.com"
  }
}
```

**Build Output:**
- Static files in `dist/` directory
- Optimized and minified assets
- Code splitting for faster loads
- Service worker for offline support (optional)

**Deployment Steps:**
1. Connect Git repository
2. Configure build settings
3. Set environment variables
4. Deploy automatically on push to main branch

---

#### Backend Deployment (Heroku/Railway/Render)

**Procfile:**
```
web: gunicorn wsgi:app
```

**Runtime Configuration:**
```
python-3.11.x
```

**Environment Variables:**
```env
GENERATIVE_API_KEY=<production_key>
SUPABASE_URL=<production_url>
SUPABASE_KEY=<production_key>
JWT_SECRET=<strong_random_secret>
FLASK_ENV=production
```

**Deployment Steps:**
1. Push code to Git repository
2. Connect to deployment platform
3. Configure environment variables
4. Set up automatic deployments
5. Configure custom domain

---

#### Database Deployment (Supabase)

**Production Configuration:**
- Enable Row-Level Security (RLS)
- Set up automated backups
- Configure connection pooling
- Enable SSL connections
- Set up monitoring and alerts

**Migration Strategy:**
```sql
-- Run migrations in order
1. Create users table
2. Create resumes table
3. Set up RLS policies
4. Create indexes
5. Seed initial data (if needed)
```

---

### CI/CD Pipeline

**GitHub Actions Workflow:**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: cd frontend && npm ci
      - name: Run linter
        run: cd frontend && npm run lint
      - name: Run tests
        run: cd frontend && npm run test
      - name: Build
        run: cd frontend && npm run build

  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: cd backend && pip install -r requirements.txt
      - name: Run tests
        run: cd backend && pytest tests/

  deploy:
    needs: [frontend-test, backend-test]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: echo "Deploy to production"
```

---

### Monitoring & Logging

#### Application Monitoring

**Frontend:**
- Error tracking: Sentry
- Analytics: Google Analytics / Plausible
- Performance: Lighthouse CI
- User behavior: Hotjar (optional)

**Backend:**
- Error tracking: Sentry
- Logging: Python logging module
- Performance: New Relic / DataDog
- Uptime monitoring: UptimeRobot

#### Log Levels

```python
DEBUG: Detailed information for debugging
INFO: General informational messages
WARNING: Warning messages for potential issues
ERROR: Error messages for failures
CRITICAL: Critical issues requiring immediate attention
```

#### Metrics to Track

**Performance Metrics:**
- API response time
- Database query time
- AI analysis duration
- File upload speed
- Page load time

**Business Metrics:**
- User registrations
- Resume uploads
- Analysis completions
- User retention
- Error rates

---

## Development Workflow

### Git Workflow

**Branch Strategy:**
```
main (production)
  ├── develop (staging)
  │   ├── feature/user-authentication
  │   ├── feature/resume-upload
  │   ├── feature/ai-analysis
  │   └── bugfix/login-error
  └── hotfix/critical-security-patch
```

**Commit Message Convention:**
```
<type>(<scope>): <subject>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Test additions/changes
- chore: Build process or auxiliary tool changes

Examples:
feat(auth): add JWT token refresh mechanism
fix(upload): resolve file size validation error
docs(api): update authentication endpoint documentation
```

---

### Code Review Process

**Pull Request Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passed
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
```

**Review Criteria:**
1. Code quality and readability
2. Test coverage
3. Performance implications
4. Security considerations
5. Documentation completeness

---

### Local Development Setup

**Prerequisites:**
- Node.js 18+ and npm
- Python 3.11+
- Git
- Code editor (VS Code recommended)

**Initial Setup:**

```bash
# Clone repository
git clone https://github.com/your-org/resume-optimizer.git
cd resume-optimizer

# Frontend setup
cd frontend
npm install
cp .env.example .env
# Edit .env with your configuration
npm run dev

# Backend setup (in new terminal)
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python wsgi.py
```

**VS Code Extensions (Recommended):**
- Vue Language Features (Volar)
- TypeScript Vue Plugin (Volar)
- Python
- Pylance
- ESLint
- Prettier
- GitLens

---

## Testing Strategy

### Frontend Testing

#### Unit Tests (Vitest)

**Component Testing:**
```typescript
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import TypingEffect from '@/components/TypingEffect.vue'

describe('TypingEffect.vue', () => {
  it('renders typing animation', () => {
    const wrapper = mount(TypingEffect)
    expect(wrapper.find('.typing-text').exists()).toBe(true)
  })

  it('displays cursor', () => {
    const wrapper = mount(TypingEffect)
    expect(wrapper.find('.cursor').exists()).toBe(true)
  })
})
```

**Store Testing:**
```typescript
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { describe, it, expect, beforeEach } from 'vitest'

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with null user', () => {
    const store = useAuthStore()
    expect(store.user).toBeNull()
  })

  it('sets token correctly', () => {
    const store = useAuthStore()
    store.setToken('test-token')
    expect(store.token).toBe('test-token')
  })
})
```

#### Integration Tests

**API Integration:**
```typescript
import { describe, it, expect, vi } from 'vitest'
import { uploadResume } from '@/api/resume'
import axios from 'axios'

vi.mock('axios')

describe('Resume API', () => {
  it('uploads resume successfully', async () => {
    const mockResponse = { data: { id: '123', score: 85 } }
    vi.mocked(axios.post).mockResolvedValue(mockResponse)

    const file = new File(['content'], 'resume.pdf')
    const result = await uploadResume(file)

    expect(result.id).toBe('123')
    expect(result.score).toBe(85)
  })
})
```

#### E2E Tests (Playwright/Cypress)

```typescript
describe('Resume Upload Flow', () => {
  it('completes full upload and analysis', () => {
    cy.visit('/login')
    cy.get('[data-test="email"]').type('user@example.com')
    cy.get('[data-test="password"]').type('password123')
    cy.get('[data-test="login-btn"]').click()

    cy.url().should('include', '/')
    cy.get('[data-test="upload-btn"]').click()

    cy.get('[data-test="file-input"]').attachFile('resume.pdf')
    cy.get('[data-test="submit-btn"]').click()

    cy.url().should('include', '/result')
    cy.get('[data-test="score"]').should('be.visible')
  })
})
```

---

### Backend Testing

#### Unit Tests (pytest)

**Route Testing:**
```python
def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_register_user(client):
    response = client.post('/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User'
    })
    assert response.status_code == 201
    assert 'token' in response.json
    assert 'user' in response.json
```

**Authentication Testing:**
```python
def test_protected_route_without_token(client):
    response = client.get('/resume/history')
    assert response.status_code == 401

def test_protected_route_with_token(client, auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.get('/resume/history', headers=headers)
    assert response.status_code == 200
```

#### Integration Tests

**Database Integration:**
```python
def test_resume_creation_and_retrieval(client, auth_token):
    # Upload resume
    with open('test_resume.pdf', 'rb') as f:
        response = client.post(
            '/resume/upload',
            data={'file': f},
            headers={'Authorization': f'Bearer {auth_token}'}
        )
    
    resume_id = response.json['id']
    
    # Retrieve resume
    response = client.get(
        f'/resume/{resume_id}/score',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    assert response.json['id'] == resume_id
```

---

### Test Coverage Goals

**Target Coverage:**
- Frontend: 80%+ code coverage
- Backend: 85%+ code coverage
- Critical paths: 100% coverage

**Coverage Reports:**
```bash
# Frontend
npm run test:coverage

# Backend
pytest --cov=api --cov-report=html
```

---

## Performance Optimization

### Frontend Optimization

#### 1. Code Splitting
```typescript
// Lazy load routes
const routes = [
  {
    path: '/upload',
    component: () => import('@/views/Upload.vue')
  },
  {
    path: '/result/:id',
    component: () => import('@/views/Result.vue')
  }
]
```

#### 2. Asset Optimization
- Image compression and lazy loading
- Font subsetting
- CSS minification
- JavaScript tree shaking
- Gzip/Brotli compression

#### 3. Caching Strategy
```typescript
// Service Worker caching
const CACHE_NAME = 'resume-optimizer-v1'
const urlsToCache = [
  '/',
  '/styles/main.css',
  '/scripts/main.js'
]
```

#### 4. Performance Metrics

**Target Metrics:**
- First Contentful Paint (FCP): < 1.5s
- Largest Contentful Paint (LCP): < 2.5s
- Time to Interactive (TTI): < 3.5s
- Cumulative Layout Shift (CLS): < 0.1
- First Input Delay (FID): < 100ms

---

### Backend Optimization

#### 1. Database Query Optimization
```python
# Use indexes
CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_resumes_created_at ON resumes(created_at DESC);

# Limit result sets
SELECT * FROM resumes WHERE user_id = ? LIMIT 50;

# Use connection pooling
```

#### 2. Caching Strategy
```python
# Redis caching (planned)
from redis import Redis
cache = Redis(host='localhost', port=6379)

def get_resume_analysis(resume_id):
    cached = cache.get(f'resume:{resume_id}')
    if cached:
        return json.loads(cached)
    
    # Fetch from database
    result = fetch_from_db(resume_id)
    cache.setex(f'resume:{resume_id}', 3600, json.dumps(result))
    return result
```

#### 3. API Response Optimization
- Gzip compression for responses
- Pagination for large datasets
- Field filtering (return only requested fields)
- ETags for conditional requests

#### 4. File Processing Optimization
- Async file processing
- Queue system for large files
- Parallel text extraction
- Streaming for large files

---

### Scalability Considerations

#### Horizontal Scaling
- Stateless API design
- Load balancer (Nginx/AWS ALB)
- Multiple backend instances
- Shared session storage (Redis)

#### Vertical Scaling
- Increase server resources
- Optimize database queries
- Upgrade database tier
- CDN for static assets

#### Database Scaling
- Read replicas for queries
- Write master for updates
- Connection pooling
- Query optimization

---

## Future Enhancements

### Phase 2: Advanced Features

#### 1. Resume Version Comparison
**Description**: Compare multiple versions of a resume side-by-side

**Technical Requirements:**
- Diff algorithm for text comparison
- Visual diff UI component
- Version history storage
- Rollback functionality

**Estimated Effort**: 2 weeks

---

#### 2. ATS Optimization
**Description**: Optimize resumes for Applicant Tracking Systems

**Features:**
- Keyword density analysis
- Format compatibility check
- Section structure validation
- ATS-friendly templates

**Technical Requirements:**
- ATS parsing simulation
- Keyword extraction algorithms
- Template engine
- PDF generation with proper structure

**Estimated Effort**: 3 weeks

---

#### 3. Job Description Matching
**Description**: Match resume against specific job descriptions

**Features:**
- Skill gap analysis
- Keyword matching score
- Tailored suggestions
- Cover letter generation

**Technical Requirements:**
- NLP for JD parsing
- Similarity algorithms
- Enhanced AI prompts
- Template system

**Estimated Effort**: 3 weeks

---

### Phase 3: Enterprise Features

#### 1. Team Collaboration
**Description**: Multiple users can collaborate on resumes

**Features:**
- Shared workspaces
- Real-time editing
- Comments and feedback
- Version control

**Technical Requirements:**
- WebSocket for real-time sync
- Operational Transform (OT) or CRDT
- Permission system
- Activity logging

**Estimated Effort**: 4 weeks

---

#### 2. Analytics Dashboard
**Description**: Comprehensive analytics for resume performance

**Features:**
- Score trends over time
- Improvement metrics
- Industry benchmarks
- Export reports

**Technical Requirements:**
- Time-series database
- Data visualization library (Chart.js/D3.js)
- Report generation
- Data aggregation pipelines

**Estimated Effort**: 3 weeks

---

#### 3. Mobile Applications
**Description**: Native mobile apps for iOS and Android

**Technology Options:**
- React Native
- Flutter
- Progressive Web App (PWA)

**Features:**
- Mobile-optimized UI
- Camera resume scanning
- Push notifications
- Offline mode

**Estimated Effort**: 8-12 weeks

---

### Phase 4: AI Enhancements

#### 1. Custom AI Models
**Description**: Train custom models for specific industries

**Features:**
- Industry-specific scoring
- Role-based analysis
- Company culture fit
- Salary prediction

**Technical Requirements:**
- ML model training pipeline
- Large dataset collection
- Model versioning
- A/B testing framework

**Estimated Effort**: 12+ weeks

---

#### 2. Interview Preparation
**Description**: AI-powered interview question generation

**Features:**
- Resume-based questions
- Mock interview simulator
- Answer evaluation
- Improvement suggestions

**Technical Requirements:**
- Question generation AI
- Speech-to-text integration
- Video recording
- Sentiment analysis

**Estimated Effort**: 6 weeks

---

## Appendix

### A. Environment Variables Reference

#### Backend (.env)
```env
# Required
GENERATIVE_API_KEY=<Google AI API key>
SUPABASE_URL=<Supabase project URL>
SUPABASE_KEY=<Supabase anon key>
JWT_SECRET=<Strong random secret>

# Optional
FLASK_ENV=development|production
PORT=8000
MAX_FILE_SIZE=10485760  # 10MB in bytes
TOKEN_EXPIRATION=86400  # 24 hours in seconds
```

#### Frontend (.env)
```env
# Optional
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Resume Optimizer
VITE_ENABLE_ANALYTICS=false
```

---

### B. Database Migration Scripts

**Initial Setup:**
```sql
-- Create users table
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create resumes table
CREATE TABLE resumes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  filename TEXT NOT NULL,
  file_path TEXT NOT NULL,
  score INTEGER CHECK (score >= 0 AND score <= 100),
  feedback TEXT,
  suggestions JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_resumes_created_at ON resumes(created_at DESC);
CREATE INDEX idx_users_email ON users(email);

-- Enable Row-Level Security
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Users can view own resumes"
ON resumes FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own resumes"
ON resumes FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own resumes"
ON resumes FOR UPDATE
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own resumes"
ON resumes FOR DELETE
USING (auth.uid() = user_id);
```

---

### C. API Rate Limiting (Planned)

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/resume/upload')
@limiter.limit("10 per hour")
@token_required
def resume_upload():
    # Upload logic
    pass
```

---

### D. Troubleshooting Guide

#### Common Issues

**Issue: CORS errors in development**
```
Solution: Ensure Flask-CORS is properly configured
Check: CORS(app, supports_credentials=True)
```

**Issue: JWT token expired**
```
Solution: Implement token refresh mechanism
Workaround: Re-login to get new token
```

**Issue: File upload fails**
```
Check: File size < 10MB
Check: File format is PDF or DOCX
Check: uploads/ directory exists and is writable
```

**Issue: AI analysis timeout**
```
Solution: Increase timeout in axios config
Check: Google AI API key is valid
Check: Network connectivity
```

---

### E. Glossary

**ATS**: Applicant Tracking System - Software used by employers to manage job applications

**CORS**: Cross-Origin Resource Sharing - Security feature controlling resource access across domains

**JWT**: JSON Web Token - Compact token format for secure information transmission

**RLS**: Row-Level Security - Database security feature restricting data access at row level

**SPA**: Single Page Application - Web app that loads single HTML page and updates dynamically

**UUID**: Universally Unique Identifier - 128-bit identifier used for unique identification

---

### F. Contact & Support

**Development Team:**
- Hugo Cui - Full-Stack Developer & Project Manager
- Julius - Full-Stack Developer (Data-focused)

**Repository:**
- GitHub: [github.com/your-org/resume-optimizer](https://github.com/your-org/resume-optimizer)

**Documentation:**
- Technical Docs: `/docs/TECHNICAL_DOCUMENTATION.md`
- API Docs: `/docs/API_DOCUMENTATION.md`
- Setup Guide: `/backend/SETUP.md`, `/frontend/SETUP.md`

---

**Document Version**: 1.0  
**Last Updated**: April 6, 2026  
**Next Review**: May 2026
