<template>
  <div class="typing-container">
    <h1 class="typing-text">
      {{ displayedText }}<span class="cursor" :class="{ blink: showCursor }">|</span>
    </h1>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const messages = [
  "Ready to land your dream job?",
  "When do we start optimizing?",
  "Your resume deserves better...",
  "Let's make recruiters notice you!",
  "Time to stand out from the crowd?",
  "Ready to level up your career?"
]

const displayedText = ref('')
const showCursor = ref(true)
const currentMessageIndex = ref(0)
const isTyping = ref(false)

let typingTimeout: number
let messageTimeout: number
let cursorInterval: number

const getRandomDelay = () => Math.floor(Math.random() * 50) + 30 // 30-80ms

const typeMessage = async (message: string) => {
  isTyping.value = true
  displayedText.value = ''
  
  for (let i = 0; i < message.length; i++) {
    displayedText.value += message[i]
    await new Promise(resolve => {
      typingTimeout = window.setTimeout(resolve, getRandomDelay())
    })
  }
  
  isTyping.value = false
  
  // Wait 3-5 seconds before next message
  const waitTime = Math.floor(Math.random() * 2000) + 3000
  messageTimeout = window.setTimeout(() => {
    fadeOutAndNext()
  }, waitTime)
}

const fadeOutAndNext = () => {
  const fadeSteps = 10
  const fadeDelay = 30
  let step = 0
  
  const fade = () => {
    step++
    if (step <= fadeSteps) {
      const textLength = displayedText.value.length
      const charsToRemove = Math.ceil(textLength / fadeSteps)
      displayedText.value = displayedText.value.slice(0, -charsToRemove)
      typingTimeout = window.setTimeout(fade, fadeDelay)
    } else {
      currentMessageIndex.value = (currentMessageIndex.value + 1) % messages.length
      typeMessage(messages[currentMessageIndex.value])
    }
  }
  
  fade()
}

onMounted(() => {
  // Start cursor blinking
  cursorInterval = window.setInterval(() => {
    showCursor.value = !showCursor.value
  }, 530)
  
  // Start typing first message
  typeMessage(messages[0])
})

onUnmounted(() => {
  clearTimeout(typingTimeout)
  clearTimeout(messageTimeout)
  clearInterval(cursorInterval)
})
</script>

<style scoped>
.typing-container {
  text-align: center;
  padding: 2rem 1rem;
}

.typing-text {
  font-size: 2.5rem;
  font-weight: 600;
  color: white;
  min-height: 3.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.cursor {
  display: inline-block;
  margin-left: 2px;
  opacity: 1;
  transition: opacity 0.1s;
}

.cursor.blink {
  opacity: 0;
}

@media (max-width: 768px) {
  .typing-text {
    font-size: 1.8rem;
    min-height: 2.5rem;
  }
}
</style>
