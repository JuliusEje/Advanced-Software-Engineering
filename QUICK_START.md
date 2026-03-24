# Resume Optimizer - Quick Start Checklist

## Pre-Deployment Checklist

### Prerequisites Setup (Do First)

- [ ] Create Supabase account and project
- [ ] Get Google Generative AI API key
- [ ] Have Node.js 16+ and Python 3.8+ installed
- [ ] Clone/have access to this repository

### Backend Setup

- [ ] Navigate to `backend/` folder
- [ ] Run `pip install -r requirements.txt`
- [ ] Create `.env` file with:
  ```env
  GENERATIVE_API_KEY=<your_google_api_key>
  SUPABASE_URL=<your_supabase_url>
  SUPABASE_KEY=<your_supabase_anon_key>
  JWT_SECRET=<create_a_random_secure_string_32+chars>
  ```
- [ ] Set up Supabase database tables:
  - [ ] Run the SQL from [backend/SETUP.md](backend/SETUP.md) to create `users` table
  - [ ] Run the SQL to create `resumes` table
  - [ ] Enable Row-Level Security policies
- [ ] Test backend: `python wsgi.py`
  - [ ] Visit `http://localhost:8000/`
  - [ ] Should see API welcome message

### Frontend Setup

- [ ] Navigate to `frontend/` folder
- [ ] Run `npm install`
- [ ] Test frontend: `npm run dev`
  - [ ] Should automatically open browser or show URL
  - [ ] Frontend should be at `http://localhost:5173` (or next available port)

### Integration Testing

With both backend and frontend running:

- [ ] **Registration**
  - [ ] Go to `/register`
  - [ ] Create new account with email/password/name
  - [ ] Should redirect to home page and show user greeting
  - [ ] Token should be in localStorage

- [ ] **Login**
  - [ ] Logout first (click Sign Out)
  - [ ] Go to `/login`
  - [ ] Login with previous credentials
  - [ ] Should redirect to home page

- [ ] **Resume Upload**
  - [ ] Go to `/upload`
  - [ ] Upload a PDF or DOCX resume file
  - [ ] Should show "Analyzing..." with loading spinner
  - [ ] After analysis, should redirect to `/result/:id`

- [ ] **Results Display**
  - [ ] Should display score (0-100)
  - [ ] Should show rating (Excellent/Good/Fair/Needs Work)
  - [ ] Should display feedback text
  - [ ] Should show 3-5 improvement suggestions
  - [ ] Should be able to upload another resume

- [ ] **Session Persistence**
  - [ ] Refresh page - should stay logged in
  - [ ] Logout and refresh - should go to home/login

### Deployment Checklist (When Ready)

#### Backend Production

- [ ] Change JWT_SECRET to a strong random value
- [ ] Set Flask `debug=False`
- [ ] Use HTTPS for all communications
- [ ] Configure CORS with specific frontend domain
- [ ] Set up environment-specific configurations
- [ ] Consider using production WSGI server (gunicorn)
- [ ] Set up monitoring and logging
- [ ] Configure database backups

#### Frontend Production

- [ ] Run `npm run build`
- [ ] Test production build locally
- [ ] Update API baseURL to production backend
- [ ] Deploy to hosting (Vercel, Netlify, etc.)
- [ ] Enable HTTPS (required for secure tokens)
- [ ] Set up CI/CD pipeline

### Troubleshooting

**Issue: Can't connect to Supabase**

- [ ] Verify SUPABASE_URL and SUPABASE_KEY are correct
- [ ] Check network connectivity
- [ ] Verify table names match SQL setup

**Issue: Upload fails with "Token required"**

- [ ] Ensure user is logged in
- [ ] Check token is in localStorage
- [ ] Verify Authorization header is being sent

**Issue: AI analysis returns error**

- [ ] Verify GENERATIVE_API_KEY is valid
- [ ] Check API quota limits in Google Cloud console
- [ ] Ensure resume file is valid PDF/DOCX

**Issue: Frontend can't reach backend**

- [ ] Ensure backend is running on port 8000
- [ ] Check CORS configuration in app.py
- [ ] Verify proxy settings in vite.config.ts

### Performance Tips

- [ ] Enable browser caching for static assets
- [ ] Consider Redis caching for user sessions (future)
- [ ] Optimize image sizes and fonts
- [ ] Use CDN for static files in production
- [ ] Monitor API response times

### Security Checklist

- [ ] Never commit .env files
- [ ] Rotate JWT_SECRET regularly
- [ ] Use HTTPS in production
- [ ] Enable CORS only for your frontend domain
- [ ] Keep dependencies updated
- [ ] Monitor for unauthorized access attempts
- [ ] Use secure password requirements

### Next Steps (Future Features)

1. **Phase 2: PDF Generation**
   - [ ] Install PyPDF2 for PDF manipulation
   - [ ] Create endpoint to generate optimized resume PDF
   - [ ] Add download button to results page

2. **Phase 3: Resume History & Comparison**
   - [ ] Implement `/resume/history` on frontend
   - [ ] Create resume card components showing past analyses
   - [ ] Add side-by-side comparison feature

3. **Phase 4: Advanced Analytics**
   - [ ] Create dashboard showing improvement trends
   - [ ] Add export functionality (CSV/PDF reports)
   - [ ] Implement resume versioning

## Support Resources

- **Backend Setup:** See [backend/SETUP.md](backend/SETUP.md)
- **Frontend Setup:** See [frontend/SETUP.md](frontend/SETUP.md)
- **Full Documentation:** See [README.md](README.md)
- **Supabase Docs:** https://supabase.com/docs
- **Vue 3 Docs:** https://vuejs.org
- **Flask Docs:** https://flask.palletsprojects.com

## Estimated Setup Time

- Prerequisites: 10-15 mins
- Backend setup: 10-15 mins
- Frontend setup: 5-10 mins
- Testing: 10-15 mins
- **Total: 35-55 minutes**

---

Once you complete all checks, your Resume Optimizer system will be fully functional and ready to help users optimize their resumes!
