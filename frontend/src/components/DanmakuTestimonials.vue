<template>
  <div class="danmaku-container">
    <div class="danmaku-stage">
      <div
        v-for="message in activeMessages"
        :key="message.id"
        class="danmaku-message"
        :style="{
          top: message.top + 'px',
          animationDuration: message.duration + 's',
          animationPlayState: message.paused ? 'paused' : 'running'
        }"
        @mouseenter="pauseMessage(message.id)"
        @mouseleave="resumeMessage(message.id)"
      >
        <span class="message-text">{{ message.text }}</span>
        <span class="message-author">— {{ message.author }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface DanmakuMessage {
  id: number
  text: string
  author: string
  top: number
  duration: number
  paused: boolean
}

const studentNames = [
  "Sarah M.", "James L.", "Emily R.", "Michael T.", "Jessica W.",
  "David K.", "Amanda P.", "Ryan C.", "Nicole H.", "Chris B.",
  "Lauren S.", "Alex J.", "Megan F.", "Daniel G.", "Rachel N."
]

const professorNames = [
  "Prof. Anderson", "Dr. Martinez", "Prof. Chen", "Dr. Williams", "Prof. Thompson"
]

const studentTestimonials = [
  "This helped me land my first internship.",
  "My CV looks way more professional now.",
  "I finally understand how to structure my resume.",
  "Super helpful for someone with no experience.",
  "Got more interview calls after using this.",
  "Makes resume building so much easier.",
  "Clear guidance, no more guessing.",
  "Saved me so much time.",
  "I wish I found this earlier.",
  "Helped me stand out among other applicants.",
  "Now I actually feel confident applying.",
  "Simple but very effective.",
  "Great for beginners.",
  "My resume finally makes sense.",
  "Really useful for JCU students."
]

const professorTestimonials = [
  "A practical tool for improving student employability.",
  "Helps students present their skills more effectively.",
  "Encourages structured and professional CV writing.",
  "A useful resource for career preparation.",
  "Supports students in building job-ready profiles."
]

const activeMessages = ref<DanmakuMessage[]>([])
let messageIdCounter = 0
let spawnInterval: number
const maxMessages = 10
const spawnDelay = 2500 // 2.5 seconds
const containerHeight = 450 // Height of danmaku area
const messageHeight = 50 // Approximate height of each message (increased)
const padding = 20 // Top and bottom padding

const getRandomTestimonial = (): { text: string; author: string } => {
  // 80% student, 20% professor
  const isStudent = Math.random() < 0.8
  
  if (isStudent) {
    const text = studentTestimonials[Math.floor(Math.random() * studentTestimonials.length)]
    const author = studentNames[Math.floor(Math.random() * studentNames.length)]
    return { text, author }
  } else {
    const text = professorTestimonials[Math.floor(Math.random() * professorTestimonials.length)]
    const author = professorNames[Math.floor(Math.random() * professorNames.length)]
    return { text, author }
  }
}

const getRandomDuration = (): number => {
  // 12-18 seconds
  return Math.random() * 6 + 12
}

const getRandomTop = (): number => {
  // Random position within container, avoiding edges
  const usableHeight = containerHeight - messageHeight - (padding * 2)
  return Math.random() * usableHeight + padding
}

const spawnMessage = () => {
  if (activeMessages.value.length >= maxMessages) {
    return
  }

  const testimonial = getRandomTestimonial()
  const newMessage: DanmakuMessage = {
    id: messageIdCounter++,
    text: testimonial.text,
    author: testimonial.author,
    top: getRandomTop(),
    duration: getRandomDuration(),
    paused: false
  }

  activeMessages.value.push(newMessage)

  // Remove message after animation completes
  setTimeout(() => {
    activeMessages.value = activeMessages.value.filter(m => m.id !== newMessage.id)
  }, newMessage.duration * 1000)
}

const pauseMessage = (id: number) => {
  const message = activeMessages.value.find(m => m.id === id)
  if (message) {
    message.paused = true
  }
}

const resumeMessage = (id: number) => {
  const message = activeMessages.value.find(m => m.id === id)
  if (message) {
    message.paused = false
  }
}

onMounted(() => {
  // Spawn initial messages with staggered timing
  for (let i = 0; i < 5; i++) {
    setTimeout(() => {
      spawnMessage()
    }, i * 600)
  }

  // Continue spawning messages
  spawnInterval = window.setInterval(() => {
    spawnMessage()
  }, spawnDelay)
})

onUnmounted(() => {
  clearInterval(spawnInterval)
})
</script>

<style scoped>
.danmaku-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 4rem 2rem;
  position: relative;
  overflow: hidden;
  min-height: 450px;
}

.danmaku-stage {
  position: relative;
  width: 100%;
  height: 450px;
  overflow: hidden;
}

.danmaku-message {
  position: absolute;
  right: -100%;
  white-space: nowrap;
  color: rgba(255, 255, 255, 0.95);
  font-size: 1.15rem;
  font-weight: 400;
  padding: 0.8rem 1.5rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 25px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  animation: slide-left linear forwards;
  cursor: default;
  user-select: none;
  transition: transform 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.danmaku-message:hover {
  transform: scale(1.05);
  background: rgba(255, 255, 255, 0.25);
}

.message-text {
  color: rgba(255, 255, 255, 0.95);
}

.message-author {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.95rem;
  font-style: italic;
}

@keyframes slide-left {
  from {
    right: -100%;
  }
  to {
    right: 110%;
  }
}

@media (max-width: 768px) {
  .danmaku-container {
    padding: 3rem 1rem;
    min-height: 350px;
  }

  .danmaku-stage {
    height: 350px;
  }

  .danmaku-message {
    font-size: 1rem;
    padding: 0.6rem 1.2rem;
  }

  .message-author {
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .danmaku-container {
    min-height: 250px;
  }

  .danmaku-stage {
    height: 250px;
  }

  .danmaku-message {
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.2rem;
  }

  .message-author {
    font-size: 0.8rem;
  }
}
</style>
