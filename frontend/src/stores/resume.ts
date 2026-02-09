import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ResumeScore } from '@/types'

export const useResumeStore = defineStore('resume', () => {
  const currentScore = ref<ResumeScore | null>(null)
  const isLoading = ref(false)

  const setScore = (score: ResumeScore) => {
    currentScore.value = score
  }

  const setLoading = (loading: boolean) => {
    isLoading.value = loading
  }

  return {
    currentScore,
    isLoading,
    setScore,
    setLoading
  }
})
