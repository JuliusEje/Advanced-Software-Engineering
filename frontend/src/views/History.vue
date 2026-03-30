<template>
  <div class="history-page">
    <nav class="navbar">
      <div class="navbar-content">
        <router-link to="/" class="nav-back">← Back to Home</router-link>
        <div class="nav-right">
          <span v-if="authStore.user" class="user-greeting">
            {{ authStore.user.name }}
          </span>
          <button @click="handleLogout" class="btn-logout">Sign Out</button>
        </div>
      </div>
    </nav>

    <div class="history-container">
      <div class="history-header">
        <h2>Your Resume History</h2>
        <p>All your previously analyzed resumes in one place</p>
        <router-link to="/upload" class="btn-upload-new">
          + Analyze New Resume
        </router-link>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading your history...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <div class="error-icon">⚠️</div>
        <p>{{ error }}</p>
        <button @click="fetchHistory" class="btn-retry">Try Again</button>
      </div>

      <!-- Empty State -->
      <div v-else-if="resumes.length === 0" class="empty-state">
        <div class="empty-icon">📄</div>
        <h3>No resumes yet</h3>
        <p>Upload your first resume to get AI-powered feedback</p>
        <router-link to="/upload" class="btn-primary">
          Upload Resume
        </router-link>
      </div>

      <!-- Resume Feed -->
      <div v-else class="resume-feed">
        <div v-for="resume in resumes" :key="resume.id" class="resume-card">
          <div class="card-header">
            <div class="file-info">
              <div class="file-icon">📄</div>
              <div class="file-details">
                <h3 class="file-name">{{ resume.filename }}</h3>
                <span class="upload-date">{{
                  formatDate(resume.created_at)
                }}</span>
              </div>
            </div>
            <div class="score-badge" :class="getScoreClass(resume.score)">
              <span class="score-number">{{ resume.score ?? "—" }}</span>
              <span class="score-label">/ 100</span>
            </div>
          </div>

          <div class="score-bar-wrapper">
            <div class="score-bar">
              <div
                class="score-fill"
                :class="getScoreClass(resume.score)"
                :style="{ width: (resume.score ?? 0) + '%' }"
              ></div>
            </div>
            <span class="score-text" :class="getScoreClass(resume.score)">
              {{ getScoreLabel(resume.score) }}
            </span>
          </div>

          <div v-if="resume.feedback" class="feedback-section">
            <h4>Feedback</h4>
            <p class="feedback-text">{{ resume.feedback }}</p>
          </div>

          <div
            v-if="resume.suggestions && resume.suggestions.length > 0"
            class="suggestions-section"
          >
            <h4>Suggestions</h4>
            <ul class="suggestions-list">
              <li
                v-for="(suggestion, index) in resume.suggestions"
                :key="index"
                class="suggestion-item"
              >
                <span class="suggestion-dot">→</span>
                {{ suggestion }}
              </li>
            </ul>
          </div>

          <div class="card-footer">
            <span class="timestamp"
              >Analyzed {{ timeAgo(resume.created_at) }}</span
            >
            <div class="card-actions">
              <button
                @click="downloadResume(resume.id, resume.filename)"
                class="btn-download"
                :disabled="downloadingId === resume.id"
              >
                <span v-if="downloadingId === resume.id">Opening...</span>
                <span v-else>⬇ Download CV</span>
              </button>
              <router-link :to="`/result/${resume.id}`" class="btn-view">
                View Full Report →
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import apiClient from "@/api/client";

interface Resume {
  id: string;
  filename: string;
  score: number | null;
  feedback: string | null;
  suggestions: string[] | null;
  created_at: string;
  updated_at: string;
}

const router = useRouter();
const authStore = useAuthStore();
const resumes = ref<Resume[]>([]);
const isLoading = ref(false);
const error = ref("");

const fetchHistory = async () => {
  isLoading.value = true;
  error.value = "";
  try {
    const response = await apiClient.get("/resume/history");
    resumes.value = response.data.resumes ?? response.data;
  } catch (err: any) {
    error.value = err.response?.data?.error || "Failed to load resume history.";
  } finally {
    isLoading.value = false;
  }
};

const handleLogout = async () => {
  await authStore.logout();
  router.push("/");
};

const formatDate = (dateStr: string): string => {
  return new Date(dateStr.replace(" ", "T")).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const timeAgo = (dateStr: string): string => {
  const diff = Date.now() - new Date(dateStr.replace(" ", "T")).getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  if (days > 0) return `${days} day${days > 1 ? "s" : ""} ago`;
  if (hours > 0) return `${hours} hour${hours > 1 ? "s" : ""} ago`;
  if (minutes > 0) return `${minutes} minute${minutes > 1 ? "s" : ""} ago`;
  return "just now";
};

const getScoreClass = (score: number | null): string => {
  if (score === null) return "score-none";
  if (score >= 80) return "score-high";
  if (score >= 50) return "score-mid";
  return "score-low";
};

const getScoreLabel = (score: number | null): string => {
  if (score === null) return "Not scored";
  if (score >= 80) return "Excellent";
  if (score >= 60) return "Good";
  if (score >= 40) return "Needs Work";
  return "Poor";
};

const downloadingId = ref<string | null>(null);

const downloadResume = async (resumeId: string, filename: string) => {
  downloadingId.value = resumeId;
  try {
    const response = await apiClient.get(`/resume/${resumeId}/download`);
    const signedUrl = response.data.url;
    // Opens PDF in new tab; browser will display or prompt download
    window.open(signedUrl, "_blank", "noopener,noreferrer");
  } catch (err) {
    console.error("Download failed:", err);
  } finally {
    downloadingId.value = null;
  }
};

onMounted(() => {
  if (!authStore.isLoggedIn) {
    router.push("/login");
    return;
  }
  fetchHistory();
});
</script>

<style scoped>
.history-page {
  min-height: 100vh;
  background: #f8f9fa;
}

.navbar {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-back {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-back:hover {
  color: #764ba2;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-greeting {
  color: #4a5568;
  font-size: 0.9rem;
}

.btn-logout {
  padding: 0.6rem 1.2rem;
  background: #e2e8f0;
  color: #2d3748;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  background: #cbd5e0;
}

.history-container {
  max-width: 800px;
  margin: 3rem auto;
  padding: 0 2rem;
}

.history-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.history-header h2 {
  font-size: 2rem;
  color: #1a202c;
  margin-bottom: 0.5rem;
}

.history-header p {
  color: #718096;
  margin-bottom: 1.5rem;
}

.btn-upload-new {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-upload-new:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.35);
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 4rem 0;
  color: #718096;
}

.spinner {
  width: 2.5rem;
  height: 2.5rem;
  border: 3px solid #e2e8f0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Error */
.error-state {
  text-align: center;
  padding: 4rem 0;
  color: #e53e3e;
}

.error-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.btn-retry {
  margin-top: 1rem;
  padding: 0.6rem 1.4rem;
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

/* Empty */
.empty-state {
  text-align: center;
  padding: 5rem 0;
  color: #718096;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #2d3748;
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
}

.btn-primary {
  display: inline-block;
  margin-top: 1.5rem;
  padding: 0.85rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.35);
}

/* Feed */
.resume-feed {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.resume-card {
  background: white;
  border-radius: 16px;
  padding: 1.75rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.07);
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}

.resume-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.11);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.file-icon {
  font-size: 2rem;
}

.file-name {
  color: #1a202c;
  font-size: 1.05rem;
  font-weight: 600;
  margin: 0 0 0.2rem;
  word-break: break-word;
}

.upload-date {
  color: #a0aec0;
  font-size: 0.85rem;
}

/* Score badge */
.score-badge {
  display: flex;
  align-items: baseline;
  gap: 2px;
  padding: 0.4rem 0.9rem;
  border-radius: 999px;
  font-weight: 700;
  flex-shrink: 0;
}

.score-number {
  font-size: 1.4rem;
}

.score-label {
  font-size: 0.8rem;
  opacity: 0.7;
}

.score-high {
  background: #c6f6d5;
  color: #276749;
}
.score-mid {
  background: #fefcbf;
  color: #744210;
}
.score-low {
  background: #fed7d7;
  color: #9b2c2c;
}
.score-none {
  background: #e2e8f0;
  color: #718096;
}

/* Score bar */
.score-bar-wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.score-bar {
  flex: 1;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}

.score-fill.score-high {
  background: #48bb78;
}
.score-fill.score-mid {
  background: #ecc94b;
}
.score-fill.score-low {
  background: #fc8181;
}
.score-fill.score-none {
  background: #cbd5e0;
}

.score-text {
  font-size: 0.8rem;
  font-weight: 600;
  min-width: 70px;
  text-align: right;
}

.score-text.score-high {
  color: #276749;
}
.score-text.score-mid {
  color: #744210;
}
.score-text.score-low {
  color: #9b2c2c;
}
.score-text.score-none {
  color: #718096;
}

/* Feedback */
.feedback-section,
.suggestions-section {
  margin-bottom: 1.25rem;
}

.feedback-section h4,
.suggestions-section h4 {
  font-size: 0.85rem;
  font-weight: 600;
  color: #4a5568;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.feedback-text {
  color: #2d3748;
  line-height: 1.7;
  font-size: 0.95rem;
  background: #f7fafc;
  padding: 1rem;
  border-radius: 8px;
  border-left: 3px solid #667eea;
}

.suggestions-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  color: #2d3748;
  font-size: 0.95rem;
  padding: 0.6rem 0.9rem;
  background: #f7fafc;
  border-radius: 8px;
}

.suggestion-dot {
  color: #667eea;
  font-weight: 700;
  flex-shrink: 0;
}

/* Footer */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.25rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.timestamp {
  color: #a0aec0;
  font-size: 0.85rem;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-download {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.45rem 1rem;
  background: #ebf4ff;
  color: #3182ce;
  border: 1px solid #bee3f8;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-download:hover:not(:disabled) {
  background: #bee3f8;
  transform: translateY(-1px);
}

.btn-download:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-view {
  color: #667eea;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: color 0.2s;
}

.btn-view:hover {
  color: #764ba2;
}

@media (max-width: 640px) {
  .history-container {
    margin: 1.5rem auto;
    padding: 0 1rem;
  }

  .card-header {
    flex-direction: column;
    gap: 1rem;
  }

  .score-badge {
    align-self: flex-start;
  }

  .card-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .card-actions {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
