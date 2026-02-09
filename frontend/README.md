# Resume Optimizer - Frontend

A modern web application built with Vue 3, TypeScript, and Vite for resume optimization and AI-powered analysis.

## Tech Stack

- **Vue 3** - Progressive JavaScript framework with Composition API
- **TypeScript** - Type-safe development
- **Vue Router** - Official routing library for Vue.js
- **Pinia** - Intuitive state management for Vue
- **Axios** - Promise-based HTTP client
- **Vite** - Next-generation frontend build tool

## Project Structure

```
frontend/
├── src/
│   ├── api/              # API service layer
│   │   └── resume.ts     # Resume-related API calls
│   ├── router/           # Vue Router configuration
│   │   └── index.ts      # Route definitions
│   ├── stores/           # Pinia state management
│   │   └── resume.ts     # Resume store
│   ├── types/            # TypeScript type definitions
│   │   └── index.ts      # Shared interfaces
│   ├── views/            # Page components
│   │   ├── Home.vue      # Landing page
│   │   ├── Upload.vue    # Resume upload page
│   │   └── Result.vue    # Score results page
│   ├── App.vue           # Root component
│   ├── main.ts           # Application entry point
│   ├── style.css         # Global styles
│   └── vite-env.d.ts     # Vite type declarations
├── index.html            # HTML entry point
├── vite.config.ts        # Vite configuration
├── tsconfig.json         # TypeScript configuration
├── tsconfig.node.json    # TypeScript config for Node
└── package.json          # Project dependencies
```

## Features

### Pages

1. **Home Page** (`/`)
   - Landing page with welcome message
   - Call-to-action button to start optimization
   - Gradient background design

2. **Upload Page** (`/upload`)
   - Drag-and-drop file upload
   - File picker for manual selection
   - Supports PDF, DOC, DOCX formats
   - Real-time upload progress
   - File validation and error handling

3. **Result Page** (`/result/:id`)
   - Visual score display (0-100)
   - Overall feedback section
   - Detailed improvement suggestions
   - Navigation back to home

### State Management

- **Resume Store** (Pinia)
  - Current score data
  - Loading states
  - Centralized state for resume operations

### API Integration

- **Base URL**: `/api` (proxied to backend)
- **Endpoints**:
  - `POST /api/resume/upload` - Upload resume file
  - `GET /api/resume/:id/score` - Fetch score results

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### Development

```bash
# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`

### Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Configuration

### Vite Configuration

The `vite.config.ts` includes:
- Vue plugin integration
- Path alias (`@` → `src`)
- Development server on port 3000
- API proxy to backend (`http://localhost:8000`)

### TypeScript Configuration

- Strict mode enabled
- ES2020 target
- Path mapping for `@/*` imports
- Vue JSX support

## Development Workflow

1. **Start Backend**: Ensure backend server is running on port 8000
2. **Start Frontend**: Run `npm run dev` in frontend directory
3. **Access Application**: Open `http://localhost:3000` in browser
4. **Hot Reload**: Changes are automatically reflected

## API Proxy

In development mode, all requests to `/api/*` are automatically proxied to `http://localhost:8000`. This is configured in `vite.config.ts`:

```typescript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

## File Upload Flow

1. User selects or drags file on Upload page
2. File validation (format, size)
3. FormData creation with file
4. POST request to `/api/resume/upload`
5. Receive response with resume ID
6. Navigate to Result page with ID
7. Fetch and display score results

## Styling

- Custom CSS with modern design
- Gradient backgrounds
- Responsive layout
- Smooth transitions and hover effects
- Mobile-friendly interface

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
