# Tools and Libraries Documentation

## Overview

This document explains all external tools, libraries, and development dependencies used in the Resume Optimizer project, including the reasoning behind each choice.

---

## Frontend Dependencies

### Core Framework

#### **Vue 3** (`^3.4.0`)

**What:** Progressive JavaScript framework for building user interfaces  
**Why Chosen:**

- ✅ Modern Composition API (better code organization than Options API)
- ✅ Excellent TypeScript support out-of-the-box
- ✅ Smaller bundle size than React (~30KB gzipped)
- ✅ Great documentation and learning curve
- ✅ Fast rendering with virtual DOM
- ✅ Single-file components (`.vue` files)

**Alternatives Considered:**

- React: More verbose, steeper learning curve
- Svelte: Smaller ecosystem, newer (risky for production)
- Angular: Too heavy for SPA, enterprise-level overkill

**Key Features Used:**

- Composition API (`<script setup>`)
- Reactive state management
- Template directives (v-if, v-for, v-bind, etc.)
- Lifecycle hooks (onMounted, onBeforeUnmount)

**Version Strategy:** Lock to `^3.4.0` for minor/patch updates

---

### Language & Type Safety

#### **TypeScript** (`^5.3.0`)

**What:** Superset of JavaScript that adds static types  
**Why Chosen:**

- ✅ Catches type errors at compile time (prevents runtime bugs)
- ✅ Excellent IDE support (autocomplete, refactoring)
- ✅ Self-documenting code (types = documentation)
- ✅ Better for team collaboration (clear interfaces)
- ✅ Required for Vue 3 best practices

**Configuration:**

```json
// tsconfig.json
{
  "strict": true, // Strict mode for all type checks
  "target": "ES2020", // Modern JavaScript target
  "module": "ESNext", // Use ES modules
  "lib": ["ES2020", "DOM"], // Include DOM types
  "jsx": "preserve" // Keep JSX for Vue
}
```

**Type Definitions Created:**

```typescript
// src/types/index.ts
export interface User {
  id: number;
  email: string;
  name: string;
}

export interface Resume {
  id: string;
  user_id: number;
  filename: string;
  score: number;
  feedback: string;
  suggestions: string[];
  created_at: string;
}
```

---

### Routing & Navigation

#### **Vue Router** (`^4.2.0`)

**What:** Official router library for Vue.js applications  
**Why Chosen:**

- ✅ Official Vue library (guaranteed compatibility)
- ✅ Seamless integration with Vue components
- ✅ Built-in route guards for authentication
- ✅ Lazy loading support for code splitting
- ✅ Nested route support for complex layouts

**Key Features Used:**

```typescript
// router/index.ts
const routes = [
  { path: "/", component: Home },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  {
    path: "/upload",
    component: Upload,
    meta: { requiresAuth: true }, // Route guard
  },
  {
    path: "/result/:id",
    component: Result,
    meta: { requiresAuth: true },
  },
];

// Route guard to protect authenticated routes
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next("/login");
  } else {
    next();
  }
});
```

**Alternatives Considered:**

- React Router: More verbose, requires different approach
- Svelte Router: Limited ecosystem

---

### State Management

#### **Pinia** (`^2.3.1`)

**What:** Official state management library for Vue 3  
**Why Chosen:**

- ✅ Smaller bundle than Vuex (~4KB vs ~15KB)
- ✅ Simpler API (less boilerplate)
- ✅ Better TypeScript support
- ✅ Easier to test (no mutations concept)
- ✅ Hot module reloading works better

**Migration from Vuex:**

- Pinia replaced Vuex (which was used in v1)
- Each store is a module (no global namespace)
- Composition API style stores

**Stores Implemented:**

```typescript
// src/stores/auth.ts
export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null);
  const token = ref<string | null>(null);
  const isAuthenticatedcomputed(() => !!token.value);

  // Actions
  const login = async (email, password) => { ... };
  const logout = () => { ... };

  // Getters
  const userEmail = computed(() => user.value?.email);

  return {
    user, token, isAuthenticated,
    login, logout, userEmail
  };
});
```

**Alternatives Considered:**

- Vuex: Older, more boilerplate
- Context API: Built-in but not as powerful
- Zustand: Good but not Vue-native

---

### HTTP Client

#### **Axios** (`^1.6.0`)

**What:** Promise-based HTTP client for making API requests  
**Why Chosen:**

- ✅ Automatic request/response interceptors (perfect for JWT)
- ✅ Built-in timeout handling
- ✅ Better error handling than `fetch`
- ✅ Request cancellation support
- ✅ Progress event for file uploads
- ✅ Can set default headers globally

**JWT Injection Pattern:**

```typescript
// src/api/client.ts
import axios from "axios";
import { useAuthStore } from "@/stores/auth";

const apiClient = axios.create({
  baseURL: "/api",
  timeout: 10000,
});

// Interceptor: Automatically add Authorization header
apiClient.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`;
  }
  return config;
});

// Interceptor: Handle 401 responses (token expired)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore().logout();
      router.push("/login");
    }
    return Promise.reject(error);
  },
);

export default apiClient;
```

**API Calls:**

```typescript
// src/api/resume.ts
export const uploadResume = async (formData: FormData) => {
  return apiClient.post("/resume/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

export const fetchResumeScore = async (resumeId: string) => {
  return apiClient.get(`/resume/${resumeId}/score`);
};
```

**Alternatives Considered:**

- `fetch` API: Less feature-rich, requires more setup
- jQuery Ajax: Outdated, heavy dependency
- Got/Needle: Node.js focused

---

### Build Tool

#### **Vite** (`^5.0.0`)

**What:** Next-generation frontend build tool and dev server  
**Why Chosen:**

- ✅ **10x faster** than Webpack (uses native ESM)
- ✅ Instant hot module replacement (HMR)
- ✅ Optimized production builds
- ✅ Out-of-the-box Vue 3 support
- ✅ Built-in TypeScript support
- ✅ Smaller bundle size via tree-shaking

**Configuration:**

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"), // @ = src folder
    },
  },
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  build: {
    minify: "terser",
    sourcemap: false, // Remove in production
    chunksizeWarningLimit: 1000,
  },
});
```

**Development Command:**

```bash
npm run dev  # Starts Vite dev server with HMR
```

**Production Build:**

```bash
npm run build  # Creates optimized /dist folder
# Result: ~150-200KB (bundle + polyfills)
```

**Alternatives Considered:**

- Webpack: Slower build times, more complex config
- Parcel: Good but less customization
- esbuild: Fast but less integrated with Vue

---

## Backend Dependencies

### Web Framework

#### **Flask** (`==2.2.3`)

**What:** Python web framework for building REST APIs  
**Why Chosen:**

- ✅ Lightweight and fast (~100 lines to start)
- ✅ Minimal dependencies (vs Django)
- ✅ Excellent for REST APIs (not just HTML templates)
- ✅ Great middleware ecosystem (Flask extensions)
- ✅ Perfect for microservices and MVPs
- ✅ Huge community support

**Project Structure:**

```
backend/
├── api/
│   ├── app.py          # Main Flask app + routes
│   ├── auth/
│   │   └── routes.py   # Auth blueprint
│   ├── models.py       # Database schemas
│   └── services/       # Business logic
├── config/
│   └── settings.py     # Configuration
├── tests/
│   └── test_app.py     # Test suite
└── wsgi.py             # Entry point
```

**Alternatives Considered:**

- Django: Overkill for API, slower development
- FastAPI: Newer (less battle-tested), overkill for MVP
- Bottle: Too minimal, less ecosystem

---

### Cloud Database & Auth

#### **Supabase** (`==2.28.3`)

**What:** PostgreSQL database with authentication and storage  
**Why Chosen:**

- ✅ PostgreSQL (industry standard relational DB)
- ✅ **Row-Level Security (RLS)** built-in
- ✅ File storage included (no separate S3 setup)
- ✅ Real-time subscriptions (future feature)
- ✅ Free tier sufficient for MVP (10K rows limit)
- ✅ Automatic backups and scaling
- ✅ API is straightforward (Python client library)

**Database Usage:**

```python
from supabase import create_client, Client

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Insert user
response = supabase.table('users').insert({
    'email': 'user@example.com',
    'name': 'John Doe',
    'password_hash': hashed
}).execute()

# Query resumes
resumes = supabase.table('resumes')\
    .select('*')\
    .eq('user_id', user_id)\
    .order('created_at', desc=True)\
    .execute()

# Upload file
supabase.storage.from_('resumes').upload(
    path=f"{user_id}/{resume_id}/resume.pdf",
    file=file_bytes
)
```

**RLS Security:**

```sql
CREATE POLICY "Users can read own resumes" ON resumes
  FOR SELECT USING (user_id = auth.uid());
```

**Alternatives Considered:**

- Firebase: Less control, proprietary, can be expensive
- MongoDB Atlas: NoSQL (overkill for structured data)
- AWS RDS + S3: More management overhead
- Heroku Postgres: No built-in RLS, separate storage

---

### AI/ML Integration

#### **Google Generative AI** (`google-genai`)

**What:** Official SDK for Google's Generative AI models (Gemini)  
**Why Chosen:**

- ✅ Free tier with generous limits (15 requests/min)
- ✅ Excellent PDF/document understanding
- ✅ Fast inference (< 2 seconds response time)
- ✅ Cost-effective ($0.075 per 1M input tokens)
- ✅ Easy integration, official library
- ✅ Multimodal (text + images + PDFs)

**Model Choice: Gemini 2.5 Flash**

- Balance of speed and quality
- Optimized for JSON output (structured responses)
- Faster than Gemini Pro (< 2s response time)
- More accurate than older models

**Usage Pattern:**

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part.from_bytes(
            data=file_bytes,
            mime_type='application/pdf'
        ),
        prompt  # Resume analysis prompt
    ]
)

# Response is JSON string
result = parse_ai_summary(response.text)
```

**Prompt Engineering:**

```python
prompt = """You are a brutally honest hiring manager in March of 2026.

Analyze this resume and respond with ONLY a valid JSON object:
{
  "score": <0-100>,
  "feedback": "<2-3 sentences>",
  "suggestions": ["<suggestion 1>", ..., "<suggestion 5>"]
}"""
```

**Alternatives Considered:**

- OpenAI (GPT-4): More expensive ($0.03-0.06 per 1K tokens)
- Claude: Better quality but slower and pricier
- LLama: Self-hosted (complexity, model maintenance)
- Azure AI: Enterprise-focused, costly

---

### Authentication & Security

#### **PyJWT** (`==2.12.1`)

**What:** JWT (JSON Web Token) creation and validation  
**Why Chosen:**

- ✅ Lightning-fast token creation/validation
- ✅ Standard library for JWT in Python
- ✅ Support for multiple signing algorithms (HS256, RS256, etc.)
- ✅ Token expiration built-in
- ✅ Payload claim validation

**JWT Implementation:**

```python
import jwt
from datetime import datetime, timedelta

def create_jwt_token(user_id, email):
    payload = {
        'user_id': user_id,
        'email': email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=24)  # 24hr expiry
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return token

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
```

**Alternatives Considered:**

- `python-jose`: More features but overkill for JWT
- `itsdangerous`: Limited to session signing, not JWT spec

---

#### **bcrypt** (`==5.0.0`)

**What:** Password hashing library with salt  
**Why Chosen:**

- ✅ Industry standard for password hashing
- ✅ Adaptive: Gets slower with each year (resists brute force)
- ✅ Automatically generates and stores salt
- ✅ Simple API (one function to hash, one to verify)
- ✅ Resistant to rainbow tables and timing attacks

**Usage:**

```python
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt(rounds=12)  # Work factor = 12 (~100ms per hash)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```

**Work Factor Tuning:**

```
rounds = 12  →  ~100ms per hash  →  Good balance
rounds = 10  →  ~10ms per hash   →  Fast but less secure
rounds = 14  →  ~1 second        →  Very slow, overkill
```

**Alternatives Considered:**

- `passlib`: Wrapper around bcrypt, additional abstraction
- `argon2`: Great but requires C library installation
- `scrypt`: Good but less standard adoption

---

### CORS & HTTP

#### **flask-cors** (`==4.0.0`)

**What:** Cross-Origin Resource Sharing (CORS) middleware for Flask  
**Why Chosen:**

- ✅ Simple decorator pattern (`@cross_origin`)
- ✅ Handles preflight requests automatically
- ✅ Configurable by route
- ✅ Supports credentials (cookies, auth headers)

**Configuration:**

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Allow credentials (JWT tokens)

# Or restrict by domain:
CORS(app, resources={
    r"/api/*": {"origins": "https://yourfrontend.com"}
})
```

**Alternatives Considered:**

- Flask's manual CORS headers: Too verbose
- Manual preflight handling: Error-prone

---

### Environment Management

#### **python-dotenv** (`==1.2.1`)

**What:** Loads environment variables from `.env` file  
**Why Chosen:**

- ✅ Never commit secrets to version control
- ✅ Different `.env` for dev/staging/production
- ✅ Clean separation of config from code
- ✅ Works seamlessly with Docker

**Usage:**

```python
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('GENERATIVE_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
JWT_SECRET = os.getenv('JWT_SECRET', 'fallback-key')  # Default if not set
```

**.env file:**

```env
# .env (never commit this file!)
GENERATIVE_API_KEY=sk_1234567890abcdef
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJhbGc...
JWT_SECRET=my-super-secret-key-32-chars-minimum
```

**.gitignore:**

```
.env
.env.local
.env.*.local
```

**Alternatives Considered:**

- `python-decouple`: Similar but less flexible
- `envirotox`: Overkill for simple needs

---

### File Handling

#### **Werkzeug** (`==2.2.3`)

**What:** WSGI utility library (included with Flask)  
**Why Chosen:**

- ✅ Already installed as Flask dependency
- ✅ `secure_filename()` prevents path traversal attacks
- ✅ File handling utilities

**Usage:**

```python
from werkzeug.utils import secure_filename

filename = request.files['file'].filename
safe_name = secure_filename(filename)
# Removes: ../, ..\\, etc. (path traversal attempts)
```

---

### Testing Framework

#### **pytest** (`installed via requirements`)

**What:** Python testing framework  
**Why Chosen:**

- ✅ Simpler syntax than `unittest`
- ✅ Fixtures for setup/teardown
- ✅ Parametrized tests
- ✅ Great assertion introspection
- ✅ Community plugins (pytest-cov for coverage)

**Test Structure:**

```python
import pytest
from api.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'message' in response.get_json()
```

---

## Development Tools

### Code Quality

#### **ESLint + Prettier** (Frontend)

- **ESLint:** Catches code quality issues
- **Prettier:** Auto-formats code (consistent style)
- **Configuration:** TypeScript + Vue support

#### **Pylint** (Backend)

- Catches code quality issues in Python
- Configurable severity levels
- IDE integration available

### Version Control

#### **Git + GitHub**

- Conventional commits format
- Branch strategy: feature branches → main
- Pull request workflow for code review

### Container & Deployment

#### **Docker & Docker Compose**

- **Docker:** Containerizes frontend + backend
- **Compose:** Runs both services + database together locally
- Benefits: Consistent dev/prod environments, easy deployment

---

## Dependency Management Strategy

### Frontend (`package.json` + `package-lock.json`)

```json
{
  "dependencies": {
    "vue": "^3.4.0", // Allow minor/patch updates
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "vite": "^5.0.0", // Dev-only tools
    "typescript": "^5.3.0"
  }
}
```

**Caret (^):**

- `^3.4.0` allows → 3.4.0, 3.5.0, 3.x.0 (not 4.0.0)
- Safer for minor updates, still flexible

**Exact versions for production:**

```
npm ci  # Install exact versions from lock file
```

### Backend (`requirements.txt`)

```
Flask==2.2.3           # Pin exact version
Werkzeug==2.2.3        # Prevents breaking changes
supabase==2.28.3
```

**Why pin versions?**

- Python libraries can have breaking changes in minor versions
- Reproducible builds across environments

---

## Summary Table

| Tool       | Purpose            | Why Chosen                        | Alternatives       |
| ---------- | ------------------ | --------------------------------- | ------------------ |
| Vue 3      | Frontend framework | Modern, TypeScript-friendly       | React, Svelte      |
| TypeScript | Type safety        | IDE support, catches errors       | Untyped JS         |
| Vite       | Build tool         | 10x faster builds                 | Webpack, Parcel    |
| Pinia      | State management   | Simple, powerful                  | Vuex, Context API  |
| Axios      | HTTP client        | JWT interceptors                  | fetch, jQuery Ajax |
| Flask      | Backend framework  | Lightweight, fast API development | Django, FastAPI    |
| Supabase   | Database & storage | RLS, free tier, PostgreSQL        | Firebase, RDS      |
| Gemini AI  | Resume analysis    | Fast, accurate, cost-effective    | GPT, Claude        |
| PyJWT      | Token management   | Standard, lightweight             | python-jose        |
| bcrypt     | Password hashing   | Industry standard                 | argon2             |
| pytest     | Testing            | Simple syntax, fixtures           | unittest           |
| Docker     | Containerization   | Consistency, deployment           | No containers      |

---
