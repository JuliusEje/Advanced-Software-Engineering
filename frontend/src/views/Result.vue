<template>
  <div class="result-page">
    <div class="result-container">
      <div v-if="loading" class="loading">Loading...</div>
      
      <div v-else-if="score" class="result-content">
        <h2>Resume Score Results</h2>
        
        <div class="score-display">
          <div class="score-circle">
            <span class="score-value">{{ score.score }}</span>
            <span class="score-max">/100</span>
          </div>
        </div>
        
        <div class="feedback-section">
          <h3>Overall Feedback</h3>
          <p>{{ score.feedback }}</p>
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getResumeScore } from '@/api/resume'
import type { ResumeScore } from '@/types'

const route = useRoute()
const router = useRouter()
const score = ref<ResumeScore | null>(null)
const loading = ref(true)

onMounted(async () => {
  const id = route.params.id as string
  try {
    score.value = await getResumeScore(id)
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})

const goBack = () => {
  router.push('/')
}
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
}

.score-value {
  font-size: 3rem;
  font-weight: bold;
}

.score-max {
  font-size: 1.2rem;
}

.feedback-section,
.suggestions-section {
  margin: 2rem 0;
}

h3 {
  color: #667eea;
  margin-bottom: 1rem;
}

.feedback-section p {
  line-height: 1.6;
  color: #555;
}

.suggestions-section ul {
  list-style: none;
  padding: 0;
}

.suggestions-section li {
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: #f5f5f5;
  border-radius: 6px;
  color: #555;
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
