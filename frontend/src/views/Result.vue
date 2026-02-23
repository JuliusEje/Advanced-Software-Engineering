<template>
  <div class="result-page">
    <div class="result-container">
      <div v-if="loading" class="loading">Loading...</div>

      <div v-else-if="score" class="result-content">
        <h2>Resume Score Results</h2>

        <div class="score-display">
          <div class="score-circle">
            <span class="score-value">{{ score.score ?? "N/A" }}</span>
            <span class="score-max">/100</span>
          </div>
        </div>

        <div class="score-bar">
          <div
            class="score-bar-fill"
            :style="{ width: ((score.score ?? 0) / 100) * 100 + '%' }"
          ></div>
        </div>

        <div class="feedback-section">
          <h3>Overall Feedback</h3>
          <p>{{ score.feedback || "No feedback available" }}</p>
        </div>

        <div class="suggestions-section">
          <h3>Improvement Suggestions</h3>
          <ul>
            <li v-for="(suggestion, index) in score.suggestions" :key="index">
              {{ suggestion }}
            </li>
          </ul>
        </div>

        <button @click="goBack" class="btn-back">Back to Home</button>
      </div>

      <div v-else class="error">
        <p>Unable to load results</p>
        <button @click="goBack" class="btn-back">Back to Home</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getResumeScore } from "@/api/resume";
import type { ResumeScore } from "@/types";

const route = useRoute();
const router = useRouter();
const score = ref<ResumeScore | null>(null);
const loading = ref(true);

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

const goBack = () => {
  router.push("/");
};
</script>

<style scoped>
.result-page {
  min-height: 100vh;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.result-container {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 700px;
  width: 100%;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #666;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.score-display {
  display: flex;
  justify-content: center;
  margin: 2rem 0;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.score-value {
  font-size: 3rem;
  font-weight: bold;
}

.score-max {
  font-size: 1.2rem;
}

.score-bar {
  width: 100%;
  height: 12px;
  background: #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
  margin: 1.5rem 0;
}

.score-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.5s ease;
}

.feedback-section,
.suggestions-section {
  margin: 2rem 0;
}

h3 {
  color: #667eea;
  margin-bottom: 1rem;
  font-size: 1.3rem;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.feedback-section p {
  line-height: 1.8;
  color: #555;
  font-size: 1rem;
  background: #f9f9f9;
  padding: 1rem;
  border-radius: 6px;
  border-left: 4px solid #667eea;
}

.suggestions-section ul {
  list-style: none;
  padding: 0;
}

.suggestions-section li {
  padding: 1rem;
  margin-bottom: 0.75rem;
  background: linear-gradient(135deg, #f5f5f5 0%, #fafafa 100%);
  border-radius: 6px;
  color: #555;
  border-left: 4px solid #667eea;
  line-height: 1.6;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.suggestions-section li:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2);
}

.btn-back {
  width: 100%;
  padding: 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 2rem;
}

.error {
  text-align: center;
}

.error p {
  color: #f44336;
  margin-bottom: 1rem;
}
</style>
