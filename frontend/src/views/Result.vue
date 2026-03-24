<template>
  <div class="result-page">
    <nav class="navbar">
      <div class="navbar-content">
        <router-link to="/" class="nav-back">← Back to Home</router-link>
        <button @click="handleLogout" class="btn-logout">Sign Out</button>
      </div>
    </nav>

    <div class="result-container">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Analyzing your resume...</p>
      </div>

      <div v-else-if="score" class="result-content">
        <div class="result-header">
          <h1>Resume Analysis Complete</h1>
          <p class="timestamp">{{ formattedDate }}</p>
        </div>

        <div class="score-section">
          <div class="score-circle">
            <span class="score-value">{{ score.score ?? "N/A" }}</span>
            <span class="score-max">/100</span>
            <span :class="['score-rating', scoreRatingClass]">{{
              scoreRating
            }}</span>
          </div>
          <div class="score-bar">
            <div
              class="score-bar-fill"
              :style="{ width: ((score.score ?? 0) / 100) * 100 + '%' }"
            ></div>
          </div>
        </div>

        <div class="feedback-section">
          <div class="section-header">
            <h2>📋 Overall Feedback</h2>
          </div>
          <p class="feedback-text">
            {{ score.feedback || "No feedback available" }}
          </p>
        </div>

        <div class="suggestions-section">
          <div class="section-header">
            <h2>💡 Improvement Suggestions</h2>
          </div>
          <div class="suggestions-grid">
            <div
              v-for="(suggestion, index) in score.suggestions"
              :key="index"
              class="suggestion-card"
            >
              <div class="suggestion-number">{{ index + 1 }}</div>
              <div class="suggestion-content">
                <p v-html="renderMarkdown(suggestion)"></p>
              </div>
            </div>
          </div>
        </div>

        <div class="actions-section">
          <button @click="goToUpload" class="btn-primary">
            Analyze Another Resume
          </button>
          <router-link to="/" class="btn-secondary"> Back to Home </router-link>
        </div>
      </div>

      <div v-else class="error-state">
        <div class="error-icon">⚠️</div>
        <h2>Unable to Load Results</h2>
        <p>We couldn't retrieve your resume analysis. Please try again.</p>
        <button @click="goBack" class="btn-primary">Back to Home</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { getResumeScore } from "@/api/resume";
import type { ResumeScore } from "@/types";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const score = ref<ResumeScore | null>(null);
const loading = ref(true);

const formattedDate = computed(() => {
  if (!score.value?.createdAt) return "";
  return new Date(score.value.createdAt).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
});

const scoreRating = computed(() => {
  const s = score.value?.score ?? 0;
  if (s >= 80) return "Excellent";
  if (s >= 70) return "Good";
  if (s >= 60) return "Fair";
  return "Needs Work";
});

const scoreRatingClass = computed(() => {
  const s = score.value?.score ?? 0;
  if (s >= 80) return "excellent";
  if (s >= 70) return "good";
  if (s >= 60) return "fair";
  return "poor";
});

onMounted(async () => {
  const id = route.params.id as string;
  try {
    score.value = await getResumeScore(id);
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
});

const goToUpload = () => {
  router.push("/upload");
};

const goBack = () => {
  router.push("/");
};

const handleLogout = async () => {
  await authStore.logout();
  router.push("/");
};

const renderMarkdown = (text: string): string => {
  if (!text) return "";
  return text
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");
};
</script>

<style scoped>
.result-page {
  min-height: 100vh;
  background: #f8f9fa;
}

.navbar {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
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

.result-container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 2rem;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  min-height: 300px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e2e8f0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  color: #718096;
  font-size: 1rem;
}

.result-content {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-header {
  text-align: center;
  margin-bottom: 2rem;
}

.result-header h1 {
  color: #1a202c;
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.timestamp {
  color: #718096;
  font-size: 0.9rem;
}

.score-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.score-circle {
  display: inline-flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
  margin-bottom: 2rem;
}

.score-value {
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1;
}

.score-max {
  font-size: 1rem;
  opacity: 0.9;
  margin-top: 0.25rem;
}

.score-rating {
  font-size: 0.85rem;
  margin-top: 0.75rem;
  padding: 0.4rem 0.8rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  font-weight: 500;
}

.score-rating.excellent {
  background: #c6f6d5;
  color: #22543d;
}

.score-rating.good {
  background: #bee3f8;
  color: #2c5282;
}

.score-rating.fair {
  background: #feebc8;
  color: #7c2d12;
}

.score-rating.poor {
  background: #fed7d7;
  color: #742a2a;
}

.score-bar {
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 1.5rem;
}

.score-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 0.75rem;
}

.section-header h2 {
  color: #1a202c;
  font-size: 1.3rem;
  margin: 0;
  font-weight: 600;
}

.feedback-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.feedback-text {
  color: #4a5568;
  line-height: 1.8;
  font-size: 1rem;
  margin: 0;
  padding: 1.5rem;
  background: #f7fafc;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.suggestions-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.suggestions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.suggestion-card {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: #f7fafc;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  transition: all 0.3s;
}

.suggestion-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.15);
  border-left-color: #764ba2;
}

.suggestion-number {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  flex-shrink: 0;
}

.suggestion-content p {
  color: #4a5568;
  margin: 0;
  line-height: 1.6;
}

.actions-section {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-primary,
.btn-secondary {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  font-size: 1rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-secondary:hover {
  background: #f7fafc;
}

.error-state {
  background: white;
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-state h2 {
  color: #1a202c;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.error-state p {
  color: #718096;
  margin-bottom: 2rem;
}

@media (max-width: 640px) {
  .result-container {
    padding: 0 1rem;
  }

  .score-circle {
    width: 140px;
    height: 140px;
  }

  .score-value {
    font-size: 2.5rem;
  }

  .suggestions-grid {
    grid-template-columns: 1fr;
  }

  .actions-section {
    flex-direction: column;
  }
}
</style>
