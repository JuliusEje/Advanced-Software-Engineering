# AI-Based Resume Analysis and Optimization Web Application

## Course Information

**Course:** CP3407 Advanced Software Engineering  
**Institution:** James Cook University (JCU)  
**Assessment:** Project Assignment  
**Team:** Group 6  
**Team Members:** Cui Langxuan, ([@Hugooooooo526](https://github.com/Hugooooooo526))
([Julius Eje](https://github.com/JuliusEje))  

**Lecturer:**([Liu Dasheng](https://github.com/DashengLIU))
**Semester:** 2026 Semester 1

---

## Project Overview

A professional web application that uses AI to analyze and optimize resumes. Features secure user authentication, session management, and detailed resume scoring with actionable improvement suggestions.

## System Architecture

The system follows a three-tier architecture consisting of:

- **Client Layer**: Vue 3 SPA handling UI and user interaction  
- **Application Layer**: Flask REST API managing business logic  
- **Data & AI Layer**: Supabase database and Google Gemini AI for resume analysis  

This architecture ensures scalability, security, and separation of concerns.

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
✓ User data isolation  
✓ Secure token storage  
✓ Protected API endpoints

## Development & Testing

### Testing
```bash
# Backend tests
cd backend
pytest tests/

# Frontend build validation
cd frontend
npm run build
npm run lint
```

### Environment Variables
Never commit `.env` files. Use `.env.example` as a template.

## Deployment

See individual setup guides:
- [Backend Deployment](backend/SETUP.md)
- [Frontend Deployment](frontend/SETUP.md)


## Support

**Team Members:**
- Cui Langxuan -(langxuan.cui@my.jcu.edu.au)- Full-stack Developer and Project Manager
- Julius Eje -(JuliusEjeanye@icloud.com)- Full-stack Developer (Data-focused)

**Course Lecturer:**
- Liu Dasheng

For technical issues or questions, please refer to the setup guides or contact the development team.



## Visual Assets(/images)

Project diagrams and design mockups are available in the `images/` folder:

### Architecture & Design Diagrams
- **[Architecture Diagram](images/architecture.png)** - System architecture visualization
- **[Entity-Relationship Diagram](images/erd.png)** - Database schema and relationships
- **[Authentication Flow](images/auth.png)** - User authentication process
- **[Upload Flow](images/upload-flow.png)** - Resume upload and analysis workflow
- **[Registration Flow](images/Registration.png)** - User registration process

### UI Design Mockups
- **[Home Page](images/UI_DESIGN_MOCKS/Home.png)** - Landing page design
- **[Login Page](images/UI_DESIGN_MOCKS/Login.png)** - User login interface
- **[Register Page](images/UI_DESIGN_MOCKS/Register.png)** - Registration interface
- **[Upload Page](images/UI_DESIGN_MOCKS/Upload.png)** - Resume upload interface
- **[Result Page](images/UI_DESIGN_MOCKS/Result.png)** - Analysis results display

---

## Documentation

Comprehensive project documentation is available in the `docs/` folder:

### Course Requirements
- **[LearnJCU Requirements](docs/learnjcu_requirement_and_rubric_file/)** - Official project requirements and assessment rubric

### Technical Documentation
- **[Architecture Design](docs/ARCHITECTURE.md)** - System architecture and component design
- **[Database Design](docs/DATABASE_DESIGN.md)** - Database schema and ER diagrams
- **[UI/UX Design](docs/UI_DESIGN.md)** - User interface design and mockups
- **[Testing Strategy](docs/TESTING_STRATEGY.md)** - Test coverage and CI/CD pipeline
- **[Tools & Libraries](docs/TOOLS_AND_LIBRARIES.md)** - Technology stack justification

### Process Documentation
- **[Agile Methodology](docs/AGILE_METHODOLOGY.md)** - Sprint planning and retrospectives
- **[Version Control](docs/VERSION_CONTROL.md)** - Git workflow and collaboration

### Requirements & Design Assets
- **[Product Requirements](docs/product_requirement_doc.txt)** - User stories and acceptance criteria
- **[Design Mockups](docs/UI_DESIGN_MOCKS/)** - Visual design assets and UI prototypes

For a complete documentation index, see [docs/README.md](docs/README.md)

---

## Project Structure

Key directories:
- `backend/` - Flask API server
- `frontend/` - Vue 3 SPA
- `docs/` - Project documentation
- `images/` - Architecture diagrams and UI mockups
- `tests/` - Test suites
