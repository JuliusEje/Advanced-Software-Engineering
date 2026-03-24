# Frontend Environment Configuration

## Setup Instructions

1. **Install Dependencies:**

   ```bash
   npm install
   ```

2. **Configure Environment (if needed):**
   - The frontend communicates with the backend at `/api`
   - Make sure your backend is running on `http://localhost:8000`
   - Update `vite.config.ts` if you need to change the backend URL

3. **Running Development Server:**

   ```bash
   npm run dev
   ```

4. **Building for Production:**
   ```bash
   npm run build
   ```

## Features Implemented

### Authentication System

- User registration with password validation
- Secure login with JWT tokens
- Session persistence using localStorage
- Token validation and refresh
- Protected routes requiring authentication

### Professional UI/UX

- Modern gradient-based color scheme (#667eea to #764ba2)
- Responsive design for mobile, tablet, and desktop
- Professional typography and spacing
- Smooth animations and transitions
- Loading states and error handling

### User Flow

1. New users register on `/register`
2. Existing users login on `/login`
3. Authenticated users access `/upload` to submit resumes
4. Results display on `/result/:id` with professional formatting
5. Users can view resume history and analyze multiple documents

### Security Features

- JWT token-based authentication
- Password hashing on backend (bcrypt)
- Protected API endpoints requiring valid tokens
- User ownership validation for resume data
- Secure token storage in localStorage

## File Structure

```
frontend/
├── src/
│   ├── views/
│   │   ├── Home.vue           # Landing page with features/benefits
│   │   ├── Login.vue          # User login
│   │   ├── Register.vue       # User registration
│   │   ├── Upload.vue         # Resume upload interface
│   │   └── Result.vue         # Analysis results display
│   ├── stores/
│   │   ├── auth.ts            # Authentication state management
│   │   └── resume.ts          # Resume data management
│   ├── api/
│   │   └── resume.ts          # API calls for resume endpoints
│   ├── router/
│   │   └── index.ts           # Vue Router with route guards
│   ├── types/
│   │   └── index.ts           # TypeScript interfaces
│   ├── App.vue                # Root component with auth initialization
│   ├── main.ts                # Application entry point
│   └── style.css              # Global styles
└── package.json               # Dependencies and scripts
```

## Data Flow

1. **Registration:** User data → Backend /auth/register → JWT token returned
2. **Login:** Credentials → Backend /auth/login → JWT token stored locally
3. **Upload Resume:** FormData + Resume file → Backend /resume/upload → Analysis performed
4. **Fetch Results:** Resume ID + Auth token → Backend /resume/{id}/score → Results displayed
5. **Resume History:** Auth token → Backend /resume/history → All user's resumes listed
