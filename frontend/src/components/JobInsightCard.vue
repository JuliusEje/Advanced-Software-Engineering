<template>
  <div class="insight-card" :style="{ opacity: cardOpacity }" @click="goToUpload">
    <div class="insight-content">
      <div class="insight-icon">🎯</div>
      <p class="insight-text">
        {{ displayedText }}<span class="cursor" :class="{ blink: showCursor }">|</span>
      </p>
    </div>
    <div class="insight-hint">Click to upload and improve →</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const jobTitles = [
  'Software Engineer',
  'Data Scientist',
  'Frontend Developer',
  'DevOps Engineer',
  'Product Manager',
  'Full Stack Developer',
  'Machine Learning Engineer',
  'Backend Developer'
]

const messageTemplates = [
  "You're so close to landing that {job} role!",
  "Almost there! That {job} position is within reach!",
  "Your next {job} opportunity is just around the corner!",
  "Keep going! You're ready for that {job} role!",
  "That {job} position? You've got this!",
  "Ready to ace that {job} interview?"
]

const displayedText = ref('')
const showCursor = ref(true)
const cardOpacity = ref(0)

let typingTimeout: number
let cursorInterval: number

const getRandomDelay = () => Math.floor(Math.random() * 50) + 30 // 30-80ms

const getRandomJob = () => jobTitles[Math.floor(Math.random() * jobTitles.length)]

const getRandomMessage = (job: string) => {
  const template = messageTemplates[Math.floor(Math.random() * messageTemplates.length)]
  return template.replace('{job}', job)
}

const typeMessage = async (message: string) => {
  displayedText.value = ''
  
  for (let i = 0; i < message.length; i++) {
    displayedText.value += message[i]
    await new Promise(resolve => {
      typingTimeout = window.setTimeout(resolve, getRandomDelay())
    })
  }
}

const goToUpload = () => {
  router.push('/upload')
}

onMounted(() => {
  // Fade in animation
  setTimeout(() => {
    cardOpacity.value = 1
  }, 100)
  
  // Start cursor blinking
  cursorInterval = window.setInterval(() => {
    showCursor.value = !showCursor.value
  }, 530)
  
  // Generate and type message
  const job = getRandomJob()
  const message = getRandomMessage(job)
  
  // Delay typing start for fade-in effect
  setTimeout(() => {
    typeMessage(message)
  }, 500)
})

onUnmounted(() => {
  clearTimeout(typingTimeout)
  clearInterval(cursorInterval)
})
</script>

<style scoped>
.insight-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  cursor: pointer;
  transition: all 0.4s ease;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.25);
  position: relative;
  overflow: hidden;
}

.insight-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0) 100%);
  opacity: 0;
  transition: opacity 0.3s;
}

.insight-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.35);
}

.insight-card:hover::before {
  opacity: 1;
}

.insight-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.insight-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.insight-text {
  color: white;
  font-size: 1.3rem;
  font-weight: 600;
  margin: 0;
  line-height: 1.5;
  min-height: 2rem;
  display: flex;
  align-items: center;
}

.cursor {
  display: inline-block;
  margin-left: 2px;
  opacity: 1;
  transition: opacity 0.1s;
  color: white;
}

.cursor.blink {
  opacity: 0;
}

.insight-hint {
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.9rem;
  text-align: right;
  font-weight: 500;
  margin-top: 0.5rem;
  transition: transform 0.3s;
}

.insight-card:hover .insight-hint {
  transform: translateX(4px);
}

@media (max-width: 640px) {
  .insight-card {
    padding: 1.5rem;
  }
  
  .insight-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .insight-text {
    font-size: 1.1rem;
  }
  
  .insight-hint {
    text-align: center;
    width: 100%;
  }
}
</style>
