# AI-Based Resume Analysis and Optimization Web Application

A professional web application that uses AI to analyze and optimize resumes. Features secure user authentication, session management, and detailed resume scoring with actionable improvement suggestions.

## Features

### 🔐 User Management

- Secure user registration and login with JWT authentication
- Session-based resume management
- Each user has access only to their own resumes
- Password hashing with bcrypt for security

### 📊 Resume Analysis

- AI-powered resume analysis using Google Generative AI
- Scoring from 0-100
- Detailed feedback on resume quality
- 3-5 actionable improvement suggestions
- Support for PDF and DOCX formats

### 🎨 Professional UI/UX

- Modern, responsive design with gradient color scheme
- Smooth animations and transitions
- Mobile-friendly interface
- Professional typography and spacing
- Intuitive user flow from registration to results

### 👤 Session-Based Features

- Resume upload tied to user accounts
- Resume history for each user
- Persistent authentication across sessions
- Secure token-based communication

## Tech Stack

### Frontend

- **Vue 3** - Progressive JavaScript framework
- **TypeScript** - Static typing for safer code
- **Vue Router** - Client-side routing with authentication guards
- **Pinia** - State management for auth and resume data
- **Vite** - Modern build tool and dev server
- **Axios** - HTTP client for API communication

### Backend

- **Flask** - Lightweight Python web framework
- **Supabase** - PostgreSQL database with authentication
- **Google Generative AI** - AI-powered resume analysis
- **JWT** - JSON Web Tokens for session management
- **Bcrypt** - Password hashing for security

### Database

- **Supabase (PostgreSQL)** with Row-Level Security
- Tables: `users`, `resumes`
- Automatic backups and scaling

## Project Structure

```
.
├── README.md
├── backend/
│   ├── SETUP.md                 # Backend setup instructions
│   ├── requirements.txt         # Python dependencies
│   ├── wsgi.py                  # WSGI entry point
│   ├── .env                     # Environment variables (not versioned)
│   ├── api/
│   │   ├── app.py              # Main Flask application
│   │   ├── models.py           # Database schemas
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   └── routes.py       # Authentication endpoints
│   │   ├── routes/
│   │   ├── utils/
│   │   └── services/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Configuration
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_app.py
│   └── uploads/                # Local resume storage
│
├── frontend/
│   ├── SETUP.md                 # Frontend setup instructions
│   ├── package.json             # npm dependencies
│   ├── vite.config.ts           # Vite configuration
│   ├── tsconfig.json            # TypeScript configuration
│   ├── index.html               # HTML entry point
│   └── src/
│       ├── main.ts              # Application entry point
│       ├── App.vue              # Root component
│       ├── style.css            # Global styles
│       ├── views/
│       │   ├── Home.vue         # Landing page
│       │   ├── Login.vue        # User login
│       │   ├── Register.vue     # User registration
│       │   ├── Upload.vue       # Resume upload
│       │   └── Result.vue       # Analysis results
│       ├── stores/
│       │   ├── auth.ts          # Auth state management
│       │   └── resume.ts        # Resume state management
│       ├── api/
│       │   └── resume.ts        # API client
│       ├── router/
│       │   └── index.ts         # Routing and guards
│       └── types/
│           └── index.ts         # TypeScript interfaces
│
├── docs/
│   └── product_requirement_doc.txt
└── .gitignore
```

## Quick Start

### Backend Setup

1. Navigate to backend directory:

   ```bash
   cd backend
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`:

   ```env
   GENERATIVE_API_KEY=your_google_api_key
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   JWT_SECRET=your-secure-secret-key
   ```

4. Set up Supabase database tables (see [Backend SETUP.md](backend/SETUP.md) for SQL)

5. Run the server:
   ```bash
   python wsgi.py
   ```

The backend will start on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start development server:

   ```bash
   npm run dev
   ```

4. Open browser to the URL shown (typically `http://localhost:5173`)

## Usage

1. **Register** - Create a new account on the registration page
2. **Login** - Sign in with your credentials
3. **Upload** - Submit a resume in PDF or DOCX format
4. **Analyze** - Wait for AI to analyze your resume
5. **Review** - Check your score, feedback, and suggestions
6. **Improve** - Make recommended changes and upload again

## API Endpoints

### Authentication

- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Sign in
- `POST /api/auth/logout` - Sign out
- `GET /api/auth/verify` - Verify token

### Resume Management

- `POST /api/resume/upload` - Upload and analyze resume
- `GET /api/resume/<id>/score` - Get resume analysis
- `GET /api/resume/history` - Get all user's resumes

## Security Features

✓ JWT token-based authentication
✓ Password hashing with bcrypt
✓ Row-Level Security (RLS) in database
✓ CORS protection
✓ User data isolation by session
✓ Secure token storage
✓ Protected API endpoints

## Future Enhancements

### Phase 2

- PDF generation for optimized resumes
- Resume version comparison
- Resume history and versioning
- Advanced analytics dashboard

### Phase 3

- ATS (Applicant Tracking System) optimization
- Industry-specific scoring models
- Job description matching
- Behavioral analysis features

### Phase 4

- Cloud file storage (AWS S3 / Google Cloud Storage)
- Redis caching for performance
- Real-time collaboration features
- Mobile native apps (React Native / Flutter)

## Database Schema

### Users Table

```sql
- id (BIGINT PRIMARY KEY)
- email (TEXT UNIQUE)
- name (TEXT)
- password_hash (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### Resumes Table

```sql
- id (UUID PRIMARY KEY)
- user_id (BIGINT FK)
- filename (TEXT)
- file_path (TEXT)
- score (INTEGER)
- feedback (TEXT)
- suggestions (JSONB)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

## Development Guidelines

### Code Quality

- Use TypeScript for type safety
- Follow Vue 3 Composition API patterns
- Use ESLint for code consistency
- Format code with Prettier

### Testing

```bash
# Frontend tests (when available)
npm run test

# Backend tests
pytest tests/
```

### Environment Variables

Never commit `.env` files. Use `.env.example` as a template.

## Deployment

See individual setup guides for deployment instructions:

- [Backend Deployment](backend/SETUP.md#deployment)
- [Frontend Deployment](frontend/SETUP.md)

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## Support

For issues or questions, please refer to the setup guides or contact the development team.

## Directory Structure (Original)

- **docs/**: Requirement documents, design specifications, and workshop reports.
- **services/**: Shared business logic modules, resume analysis pipelines, and JD-processing utilities.
- **storage/**: Persistence adapters, migration scripts, and history management assets.
- **infrastructure/**: Deployment and environment configuration (e.g., Dockerfiles, IaC templates).
- **tests/**: Automated test suites covering frontend, backend, and service integrations.
- **data/**: Sample resumes and job descriptions for development and testing (ignored by version control).
- **scripts/**: Developer utilities for setup, linting, data preparation, and CI/CD tasks.
