# UI/UX Design

## Design Philosophy

**Principle:** Minimalist, professional, gradient-based design that guides users through a smooth resume optimization journey.

**Color Scheme:**

- **Primary Gradient:** #667eea (indigo) → #764ba2 (purple)
- **Background:** #f8f9fa (light gray)
- **Success:** #10b981 (emerald)
- **Warning/Error:** #ef4444 (red)
- **Text:** #2d3748 (dark gray)

**Typography:**

- **Font Family:** -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto" (system fonts for fast loading)
- **Headings:** Bold, 1.5-2rem, high contrast
- **Body:** Regular 0.875-1rem, readable line-height (1.5)

**Responsive Design:**

- Mobile-first approach
- Breakpoints: 640px (tablet), 1024px (desktop)
- Touch-friendly buttons: min 44x44px

---

## Page Layouts

### 1. Home Page (`/`)

**Purpose:** Landing page, feature showcase, brand messaging

**Layout Description:**

```
┌─────────────────────────────────────────────────────┐
│                    NAVBAR                           │
│  ← Resume Optimizer        [Sign Out] / [Login]     │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│                  HERO SECTION                        │
│  📄 Optimize Your Resume with AI                    │
│  "Get instant feedback and actionable suggestions   │
│   to make your resume stand out"                    │
│                                                      │
│        ┌──────────────────────────────┐             │
│        │ Get Started (CTA Button)     │             │
│        └──────────────────────────────┘             │
│                                                      │
│  [Gradient Background - Indigo to Purple]           │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│                FEATURES SECTION                      │
│  🚀 Quick Analysis   ⚡ AI-Powered   📊 Score 0-100 │
│  🔐 Secure & Private 💡 Actionable  📱 Responsive   │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│              TESTIMONIALS CAROUSEL                   │
│  "Great tool! Got hired 2 weeks after optimizing"  │
│  "The suggestions were spot-on and specific"        │
│  "Love how intuitive the interface is"              │
│  [← Carousel nav →]                                 │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│                  CALL TO ACTION                      │
│  Ready to optimize your resume?                     │
│        [Get Started Now]                            │
└─────────────────────────────────────────────────────┘
```

**Key Components:**

- **Navigation Bar:** Logo, sign out button, responsive hamburger menu
- **Hero Section:** Large heading, supporting text, primary CTA button
- **Features Grid:** 3-6 feature cards with icons
- **Testimonials:** Carousel with quote/name/title
- **Footer:** CTA button, links, copyright

**Design Notes:**

- Smooth scroll-triggered animations
- Gradient background extends across hero
- Cards have subtle shadow on hover
- Call-to-action buttons use primary gradient with scale transform

---

### 2. Login Page (`/login`)

**Purpose:** User authentication, credential entry

**Layout Description:**

```
┌─────────────────────────────────────────────────────┐
│              Return to Home Link                     │
│                    ← Back                            │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│                                                      │
│              LOGIN PAGE (Centered)                   │
│                                                      │
│  Resume Optimizer                                   │
│  Sign In to Your Account                            │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Email                                         │  │
│  │ [________________________________________]   │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Password                                      │  │
│  │ [________________________________________]   │  │
│  │                                         👁 (show/hide) │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ☐ Remember me                                      │
│                                                      │
│  ┌─ [Login] ──────────────────────────────────┐   │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Don't have an account? [Sign Up]                  │
│  [Forgot Password?]                                 │
│                                                      │
│  Error Message (if invalid credentials):            │
│  ⚠ Invalid email or password                       │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Key Components:**

- **Input Fields:** Email, password (masked)
- **Validation Indicators:** Green checkmark if email format valid
- **Error Display:** Red text below field for inline errors
- **Loading State:** Button shows spinner while authenticating
- **Links:** Sign up, forgot password, back to home

**Form Validation:**

```
Email:
  ├─ Required
  ├─ Valid format (user@example.com)
  └─ Visual feedback: ✓ green or ✗ red

Password:
  ├─ Required
  ├─ Min 8 characters
  └─ Show/hide toggle
```

---

### 3. Register Page (`/register`)

**Purpose:** New user account creation

**Layout Description:**

```
┌─────────────────────────────────────────────────────┐
│              ← Back to Home                          │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│                                                      │
│           REGISTRATION PAGE (Centered)              │
│                                                      │
│  Join Resume Optimizer Today                        │
│  Create Your Free Account                           │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Full Name                                     │  │
│  │ [________________________________________]   │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Email Address                                 │  │
│  │ [________________________________________]   │  │
│  │ ☐ This email is available                   │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Password                                      │  │
│  │ [________________________________________]   │  │
│  │ Password Strength: ████░░░░░░ Medium         │  │
│  │ Must contain: 8+ chars, uppercase, number   │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Confirm Password                              │  │
│  │ [________________________________________]   │  │
│  │ ✓ Passwords match                            │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ☐ I agree to Terms of Service                     │
│                                                      │
│  ┌─ [Create Account] ──────────────────────────┐   │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Already have an account? [Login]                   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Key Components:**

- **Input Fields:** Name, email, password (2 fields)
- **Real-time Validation:**
  - Email uniqueness check (debounced)
  - Password strength meter
  - Password match confirmation
- **Terms Checkbox:** Required before registration
- **Loading State:** Button disabled + spinner

**Validation Rules:**

```
Name:
  ├─ Required
  └─ 2-50 characters

Email:
  ├─ Required
  ├─ Valid format
  ├─ Not already registered
  └─ Real-time availability check

Password:
  ├─ Required
  ├─ ≥8 characters
  ├─ ≥1 uppercase letter
  └─ ≥1 number
```

---

### 4. Upload Page (`/upload`)

**Purpose:** Resume file submission and optional JD input

**Layout Description:**

```
┌─────────────────────────────────────────────────────┐
│ ← Back to Home            Welcome, [Name]  [Sign Out]│
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│                                                      │
│          UPLOAD YOUR RESUME                         │
│  "We'll analyze it and provide detailed feedback"   │
│                                                      │
│  ┌──────────────────┬──────────────────────────┐   │
│  │                  │                          │   │
│  │   JOB DETAILS    │    RESUME UPLOAD         │   │
│  │   (Optional)     │                          │   │
│  │                  │                          │   │
│  │ Company:         │   ┌──────────────────┐   │   │
│  │ [Google    ──]   │   │  📄              │   │   │
│  │                  │   │                  │   │   │
│  │ Job Description: │   │ Drag & drop here │   │   │
│  │ [              ]  │   │ or              │   │   │
│  │ [              ]  │   │ [Choose File]   │   │   │
│  │ [              ]  │   │                  │   │   │
│  │ Paste JD here...  │   │ PDF, DOCX       │   │   │
│  │ [              ]  │   │ Max 10MB        │   │   │
│  │ [              ]  │   │                  │   │   │
│  │                  │   └──────────────────┘   │   │
│  │                  │   ✓ resume.pdf (2.5MB)  │   │
│  │                  │   [× Clear]              │   │
│  │                  │                          │   │
│  └──────────────────┴──────────────────────────┘   │
│                                                      │
│             ┌──────────────────────────┐            │
│             │ Upload & Analyze (CTA)  │            │
│             │ [Loading...] (when active)           │
│             └──────────────────────────┘            │
│                                                      │
│  ⓘ Analyzing your resume...                        │
│    [████████░░░░░░░░░░] 50% complete               │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Key Components:**

- **Two-Column Layout:**
  - Left: Job Description (optional section)
    - Company name input
    - Job description textarea
  - Right: Resume upload area
    - Drag-and-drop zone
    - File picker button
    - File validation feedback
- **Drag-and-Drop Interaction:**
  - Highlight zone on drag over
  - Accept PDF, DOCX only
  - Size validation (< 10MB)
- **Upload Progress:**
  - Progress bar
  - Status message: "Analyzing..."
  - Estimated time

**Validations:**

```
Resume File:
  ├─ Required
  ├─ Type: PDF or DOCX only
  ├─ Size: < 10 MB
  └─ Not corrupted (readable)

Job Description:
  ├─ Optional
  ├─ Max 5000 characters
  └─ Used for match scoring
```

---

### 5. Result Page (`/result/:id`)

**Purpose:** Display resume analysis results and suggestions

**Layout Description:**

```
┌─────────────────────────────────────────────────────┐
│ ← Back to Home            Welcome, [Name]  [Sign Out]│
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│                                                      │
│        Resume Analysis Complete                     │
│        March 10, 2026 at 2:45 PM                    │
│                                                      │
│  ┌──────────────────┬──────────────────────────┐   │
│  │                  │                          │   │
│  │  SCORE SECTION   │   JD INFO (if provided)  │   │
│  │                  │                          │   │
│  │  ┌────────────┐  │  🏢 Target Position      │   │
│  │  │            │  │  Company: Google         │   │
│  │  │    82      │  │  Role: Senior Engineer   │   │
│  │  │   /100     │  │                          │   │
│  │  │            │  │  Match Score: 82/100     │   │
│  │  │  GOOD ✓    │  │                          │   │
│  │  └────────────┘  │                          │   │
│  │  Resume Score    │                          │   │
│  │                  │  [████████░] 82%         │   │
│  │                  │                          │   │
│  └──────────────────┴──────────────────────────┘   │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │ 📋 OVERALL FEEDBACK                         │   │
│  │                                             │   │
│  │ Your resume effectively highlights your    │   │
│  │ technical expertise and leadership skills. │   │
│  │ The format is clean and professional, but  │   │
│  │ lacks quantifiable metrics for your major  │   │
│  │ achievements.                              │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │ 💡 IMPROVEMENT SUGGESTIONS                  │   │
│  │                                             │   │
│  │ ┌─ 1. Add quantifiable metrics ──────────┐ │   │
│  │ │ Include specific numbers for impact    │ │   │
│  │ │ (e.g., "increased sales by 25%")      │ │   │
│  │ └─────────────────────────────────────────┘ │   │
│  │                                             │   │
│  │ ┌─ 2. Expand technical skills ──────────┐ │   │
│  │ │ Add 2-3 more relevant frameworks      │ │   │
│  │ │ and programming languages             │ │   │
│  │ └─────────────────────────────────────────┘ │   │
│  │                                             │   │
│  │ ┌─ 3. Strengthen action verbs ─────────┐ │   │
│  │ │ Replace "Worked on" with "Led"       │ │   │
│  │ │ or "Architected"                      │ │   │
│  │ └─────────────────────────────────────────┘ │   │
│  │                                             │   │
│  │ ┌─ 4. Add a professional summary ─────┐ │   │
│  │ │ 2-3 lines at top highlighting key   │ │   │
│  │ │ qualifications                       │ │   │
│  │ └─────────────────────────────────────────┘ │   │
│  │                                             │   │
│  │ ┌─ 5. Format for ATS compatibility ───┐ │   │
│  │ │ Use standard sections, avoid tables  │ │   │
│  │ │ for better parsing                   │ │   │
│  │ └─────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ [Analyze Another Resume] [Back to Home]     │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Key Components:**

- **Score Circle:** Prominent, gradient-filled circle showing score 0-100
- **Rating Badge:** "Excellent", "Good", "Fair", or "Needs Work"
- **Progress Bar:** Visual representation of score percentage
- **Feedback Section:**
  - Main feedback text (2-3 sentences)
  - Clear, honest, constructive language
- **Suggestion Cards:**
  - Numbered (1-5)
  - Icon + title + description
  - Specific, actionable advice
  - Collapsible for mobile
- **Action Buttons:**
  - "Analyze Another Resume" → navigate to /upload
  - "Back to Home" → navigate to /
  - Optional: "Download as PDF" (future)

**Data Visualization:**

```
Score Circle:
├─ Color gradient based on score
│  ├─ 0-30: Red (#ef4444)
│  ├─ 30-60: Yellow (#f59e0b)
│  └─ 60-100: Green (#10b981)
└─ Animated on page load (0 → final score)

Progress Bar:
├─ Width represents percentage
├─ Smooth animation (0% → 100%)
└─ Color matches score circle
```

---

### 6. History Page (`/history`) - Future

**Layout Description:**

```
┌─────────────────────────────────────────────────────┐
│ ← Back to Home            Welcome, [Name]  [Sign Out]│
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│                                                      │
│  YOUR RESUME HISTORY                                │
│  [Filter by date ▼] [Sort by score ▼]              │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Resume 1                    Score: 85/100    │  │
│  │ uploaded_resume_v3.pdf      March 10, 2026   │  │
│  │ [View Details]              [Download]       │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Resume 2                    Score: 72/100    │  │
│  │ resume_2025_final.pdf       Feb 28, 2026     │  │
│  │ [View Details]              [Download]       │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Resume 3                    Score: 68/100    │  │
│  │ my_resume.docx              Feb 15, 2026     │  │
│  │ [View Details]              [Compare v1]     │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Component Library

### 1. Button Component

**States:**

- **Default:** Gradient background, white text, shadow
- **Hover:** Slightly darker gradient, scale transform (1.05)
- **Active:** Pressed appearance (scale 0.98)
- **Disabled:** Opacity 0.5, cursor not-allowed
- **Loading:** Shows spinner, text dims

**Sizes:**

- Small: 8px padding, 0.875rem text
- Medium: 12px padding, 1rem text
- Large: 16px padding, 1.125rem text

### 2. Input Field Component

**States:**

- **Default:** Border #e5e7eb, cursor auto
- **Focus:** Border gradient color, outline none, shadow
- **Valid:** Green border checkmark, #10b981
- **Error:** Red border, error message below, #ef4444
- **Disabled:** Background #f3f4f6, cursor not-allowed

**Validation Indicators:**

- ✓ Green: Valid input
- ✗ Red: Invalid input
- ⓘ Blue: Info tooltip

### 3. Card Component

**Properties:**

- Background: white
- Border: 1px #e5e7eb
- Border-radius: 8px
- Padding: 16px
- Box-shadow: 0 1px 3px rgba(0,0,0,0.1)
- Hover: Shadow increased, subtle scale

### 4. Loading Spinner

```
Animated circular progress indicator
├─ Size: 24px (small), 40px (medium), 64px (large)
├─ Color: Gradient from primary to secondary
├─ Animation: 1.5s rotation, infinite loop
└─ Used in: Upload progress, form submission
```

### 5. Progress Bar

```
├─ Height: 4px
├─ Background: #e5e7eb
├─ Fill: Gradient primary to secondary
├─ Animation: smooth width transition (300ms)
└─ Shows percentage label
```

---

## Responsive Design Breakpoints

```css
/* Mobile-first approach */
@media (min-width: 640px) {
  /* Tablet: 640px+ */
  /* Two-column layouts become possible */
}

@media (min-width: 1024px) {
  /* Desktop: 1024px+ */
  /* Three-column layouts, increased padding */
}

@media (min-width: 1280px) {
  /* Large desktop: 1280px+ */
  /* Max-width container, sidebar layouts */
}
```

**Mobile Adjustments:**

- Font sizes: -4px on mobile
- Padding: Reduced by 50%
- Column layouts → Stack vertically
- Buttons: Full-width (100%)
- Minimum touch target: 44x44px

---

## Accessibility Standards

| Standard                | Implementation                                |
| ----------------------- | --------------------------------------------- |
| **WCAG 2.1 Level AA**   | High contrast ratios (4.5:1 text), sufficient |
| **Keyboard Navigation** | All interactive elements focusable (Tab key)  |
| **Screen Reader**       | Semantic HTML, ARIA labels where needed       |
| **Color**               | Not sole indicator (use icons + text)         |
| **Focus Indicators**    | Visible focus ring (outline-width: 2px)       |
| **Form Labels**         | Associated with inputs (`<label for>`)        |

---
