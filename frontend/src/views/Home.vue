<template>
  <div class="home">
    <nav class="navbar">
      <div class="navbar-content">
        <div class="logo">
          <h2>Resume Optimizer</h2>
        </div>
        <div class="nav-actions">
          <span v-if="authStore.user" class="user-greeting">
            Welcome, {{ authStore.user.name }}
          </span>
          <button
            v-if="authStore.isAuthenticated"
            @click="handleLogout"
            class="btn-logout"
          >
            Sign Out
          </button>
          <router-link
            v-if="authStore.isAuthenticated"
            to="/history"
            class="btn-nav"
          >
            History
          </router-link>
          <router-link v-else to="/login" class="btn-nav">
            Sign In
          </router-link>
        </div>
      </div>
    </nav>

    <div class="hero-section">
      <div class="hero-content">
        <h1>Optimize Your Resume with AI</h1>
        <p class="hero-subtitle">
          Get professional feedback and actionable suggestions to make your CV
          stand out
        </p>

        <button
          v-if="authStore.isAuthenticated"
          @click="goToUpload"
          class="btn-primary"
        >
          Upload & Analyze Resume
        </button>
        <router-link v-else to="/register" class="btn-primary">
          Get Started
        </router-link>
      </div>
    </div>

    <div class="features-section">
      <h2>How It Works</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">📋</div>
          <h3>Upload Your Resume</h3>
          <p>Submit your resume in PDF or DOCX format</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🤖</div>
          <h3>AI Analysis</h3>
          <p>Our AI analyzes your resume for quality and completeness</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>Get Score & Feedback</h3>
          <p>Receive a detailed score and personalized suggestions</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">✨</div>
          <h3>Improve & Track</h3>
          <p>Access your history and track improvements over time</p>
        </div>
      </div>
    </div>

    <div class="benefits-section">
      <h2>Why Choose Resume Optimizer?</h2>
      <div class="benefits-list">
        <div class="benefit-item">
          <span class="check-mark">✓</span>
          <div>
            <h4>Professional Standards</h4>
            <p>Analyze resumes against industry best practices</p>
          </div>
        </div>
        <div class="benefit-item">
          <span class="check-mark">✓</span>
          <div>
            <h4>Actionable Insights</h4>
            <p>Get specific, immediately applicable recommendations</p>
          </div>
        </div>
        <div class="benefit-item">
          <span class="check-mark">✓</span>
          <div>
            <h4>Secure & Private</h4>
            <p>Your resume data is encrypted and securely stored</p>
          </div>
        </div>
        <div class="benefit-item">
          <span class="check-mark">✓</span>
          <div>
            <h4>Save & Compare</h4>
            <p>Access all your previous analyses anytime</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const goToUpload = () => {
  router.push("/upload");
};

const handleLogout = async () => {
  await authStore.logout();
  router.push("/");
};
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: #f8f9fa;
}

.navbar {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.navbar-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo h2 {
  color: #667eea;
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.user-greeting {
  color: #4a5568;
  font-size: 0.9rem;
}

.btn-nav,
.btn-logout {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
  border: none;
  text-decoration: none;
  display: inline-block;
}

.btn-nav {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-nav:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-logout {
  background: #e2e8f0;
  color: #2d3748;
}

.btn-logout:hover {
  background: #cbd5e0;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 6rem 2rem;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-section h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.95;
  line-height: 1.6;
}

.btn-primary {
  display: inline-block;
  padding: 1rem 2.5rem;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.features-section {
  max-width: 1200px;
  margin: 4rem auto;
  padding: 0 2rem;
}

.features-section h2 {
  font-size: 2.5rem;
  color: #1a202c;
  text-align: center;
  margin-bottom: 3rem;
  font-weight: 700;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  text-align: center;
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #1a202c;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.feature-card p {
  color: #718096;
  line-height: 1.6;
}

.benefits-section {
  background: white;
  padding: 4rem 2rem;
  margin-top: 4rem;
}

.benefits-section h2 {
  font-size: 2.5rem;
  color: #1a202c;
  text-align: center;
  margin-bottom: 3rem;
  font-weight: 700;
}

.benefits-list {
  max-width: 900px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.benefit-item {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.check-mark {
  flex-shrink: 0;
  font-size: 1.5rem;
  color: #667eea;
  font-weight: 700;
}

.benefit-item h4 {
  color: #1a202c;
  margin-bottom: 0.5rem;
}

.benefit-item p {
  color: #718096;
  margin: 0;
}

@media (max-width: 768px) {
  .navbar-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .hero-section {
    padding: 4rem 1rem;
  }

  .hero-section h1 {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .features-section h2,
  .benefits-section h2 {
    font-size: 1.8rem;
  }
}
</style>
